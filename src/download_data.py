"""
Download daily total-return series for every AP5 sleeve and bond-replacement proxy from
the Yahoo Finance chart API (via requests + the agent-proxy CA bundle), convert non-CHF
proxies to CHF, splice the CLO series, and synthesize CHF cash and ILS.

Output:
  data/raw/<ticker>.csv            (raw adjclose per instrument, native ccy)
  data/processed/prices_chf.csv    (all sleeves+candidates as CHF total-return indices)
  data/processed/returns_daily.csv (daily simple returns, CHF)

Run:  python src/download_data.py
"""
from __future__ import annotations
import os, time, json
import numpy as np
import pandas as pd
import requests

from config import PROXIES, FX, START, END, SNB_PATH, USD_PATH, HEDGE_TO_CHF

CA = "/root/.ccr/ca-bundle.crt"
os.environ.setdefault("REQUESTS_CA_BUNDLE", CA)
os.environ.setdefault("SSL_CERT_FILE", CA)
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(HERE, "data", "raw")
PROC = os.path.join(HERE, "data", "processed")
os.makedirs(RAW, exist_ok=True)
os.makedirs(PROC, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0"})


def fetch_yahoo(ticker: str, tries: int = 4) -> pd.Series:
    """Daily adjusted-close (total return) series for a ticker, indexed by date."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?range=10y&interval=1d&events=div,splits")
    last_err = None
    for k in range(tries):
        try:
            r = SESSION.get(url, timeout=30)
            r.raise_for_status()
            res = r.json()["chart"]["result"][0]
            ts = res["timestamp"]
            q = res["indicators"]["quote"][0]
            adj = (res["indicators"].get("adjclose", [{}])[0].get("adjclose")
                   if "adjclose" in res["indicators"] else None)
            close = adj if adj is not None else q["close"]
            idx = pd.to_datetime(ts, unit="s").normalize()
            s = pd.Series(close, index=idx, name=ticker).dropna()
            s = s[~s.index.duplicated(keep="last")].sort_index()
            return s
        except Exception as e:                       # pragma: no cover
            last_err = e
            time.sleep(2 ** k)
    raise RuntimeError(f"failed {ticker}: {last_err}")


def build_cash(index: pd.DatetimeIndex) -> pd.Series:
    """Synthetic CHF cash total-return index from the SNB policy-rate path.
    Daily accrual = rate/360. Captures the negative-rate drag 2019-2022."""
    steps = pd.DataFrame(SNB_PATH, columns=["date", "rate"])
    steps["date"] = pd.to_datetime(steps["date"])
    rate = (steps.set_index("date")["rate"].reindex(index, method="ffill")
            .fillna(steps["rate"].iloc[0]) / 100.0)
    daily = rate / 360.0
    lvl = (1.0 + daily).cumprod()
    return (lvl / lvl.iloc[0]).rename("cash")


def _rate_path(path, index) -> pd.Series:
    steps = pd.DataFrame(path, columns=["date", "rate"])
    steps["date"] = pd.to_datetime(steps["date"])
    return (steps.set_index("date")["rate"].reindex(index, method="ffill")
            .fillna(steps["rate"].iloc[0]) / 100.0)


def to_chf(s: pd.Series, ccy: str, fx: dict[str, pd.Series]) -> pd.Series:
    """Convert a native-currency total-return series into CHF terms (UNHEDGED, spot)."""
    if ccy == "CHF":
        return s
    f = fx[ccy].reindex(s.index).ffill()
    return (s * f).dropna()


def to_chf_hedged(s: pd.Series, ccy: str) -> pd.Series:
    """CHF-hedged total return: keep the native-currency (local) return and add the
    daily hedge carry (r_CHF - r_foreign)/252. Removes FX spot moves, retains the
    interest-rate-differential cost the draft flags (~0.5-1.5% p.a.)."""
    loc = s.pct_change().dropna()
    r_chf = _rate_path(SNB_PATH, loc.index)
    r_for = _rate_path(USD_PATH if ccy == "USD" else USD_PATH, loc.index)
    carry = (r_chf - r_for) / 252.0
    hedged = (1 + loc + carry).cumprod()
    return (100 * hedged / hedged.iloc[0]).reindex(s.index).ffill()


def main():
    # ---- fetch everything -----------------------------------------------------
    fx = {}
    for ccy, tk in FX.items():
        try:
            fx[ccy] = fetch_yahoo(tk).rename(ccy)
            fx[ccy].to_csv(os.path.join(RAW, f"FX_{ccy}.csv"))
            print(f"FX {ccy:3} {tk:10} {fx[ccy].index.min().date()}->{fx[ccy].index.max().date()}")
        except Exception as e:
            print("FX FAIL", ccy, e)

    raw = {}
    for name, cfg in PROXIES.items():
        try:
            s = fetch_yahoo(cfg["ticker"])
            s.to_csv(os.path.join(RAW, f"{cfg['ticker']}.csv"))
            raw[name] = s
            print(f"{name:16} {cfg['ticker']:10} {cfg['ccy']} "
                  f"{s.index.min().date()}->{s.index.max().date()} n={len(s)}")
            time.sleep(0.2)
        except Exception as e:
            print("FAIL", name, cfg["ticker"], e)

    # ---- convert to CHF -------------------------------------------------------
    chf = {}
    for name, cfg in PROXIES.items():
        if name.startswith("_") or name not in raw:
            continue
        if name in HEDGE_TO_CHF and cfg["ccy"] != "CHF":
            chf[name] = to_chf_hedged(raw[name], cfg["ccy"])   # CHF-hedged share class
        else:
            chf[name] = to_chf(raw[name], cfg["ccy"], fx)       # CHF-native or unhedged

    # ---- splice CLO (JAAA) backward with FLOT for pre-2020-10 window ----------
    # Chain daily returns: FLOT (hedged) before JAAA's start, JAAA (hedged) after.
    if "clo" in chf and "_flot" in raw:
        jaaa = chf["clo"]
        flot = to_chf_hedged(raw["_flot"], PROXIES["_flot"]["ccy"])  # hedged, matches clo
        start_j = jaaa.index.min()
        if start_j > pd.Timestamp(START):
            jaaa_ret = jaaa.pct_change().dropna()
            flot_ret = flot.pct_change()[flot.index < start_j].dropna()
            # Dampen the FLOT backfill to JAAA's own (much lower) daily vol, keeping its
            # trend. FLOT is leveraged/liquidity-sensitive (its Mar-2020 dislocation was
            # ~-12% vs AAA CLO's real ~-3 to -5%); compressing to JAAA vol avoids
            # overstating AAA-CLO crisis risk in the 2019-07->2020-10 backfill window.
            mu, sd = flot_ret.mean(), flot_ret.std()
            scale = jaaa_ret.std() / sd if sd > 0 else 1.0
            flot_ret = mu + (flot_ret - mu) * scale
            ret = pd.concat([flot_ret, jaaa_ret]).dropna()
            ret = ret[~ret.index.duplicated(keep="last")].sort_index()
            lvl = (1 + ret).cumprod()
            chf["clo"] = (100 * lvl / lvl.iloc[0])
            print(f"CLO spliced with FLOT: {chf['clo'].index.min().date()}"
                  f"->{chf['clo'].index.max().date()} n={len(chf['clo'])}")

    # ---- align to business-day grid over the window --------------------------
    all_idx = pd.bdate_range(START, END)
    price = pd.DataFrame(index=all_idx)
    for name, s in chf.items():
        price[name] = s.reindex(all_idx).ffill()

    # ---- synthetic CHF cash ---------------------------------------------------
    price["cash"] = build_cash(all_idx)

    # ---- synthetic ILS (built in separate module to keep provenance explicit) -
    from synth_ils import build_ils
    price["ils"] = build_ils(all_idx, SNB_PATH)

    # rebase each series to 100 at first valid obs, trim leading NaNs
    price = price.dropna(how="all")
    price = price.loc[price.index >= pd.Timestamp(START)]
    price = price.ffill().dropna()
    price = price / price.iloc[0] * 100.0

    rets = price.pct_change().dropna()
    price.to_csv(os.path.join(PROC, "prices_chf.csv"))
    rets.to_csv(os.path.join(PROC, "returns_daily.csv"))
    print("\nSaved prices_chf.csv", price.shape, "and returns_daily.csv", rets.shape)
    print("Columns:", list(price.columns))
    print(price.tail(2).round(2).to_string())


if __name__ == "__main__":
    main()
