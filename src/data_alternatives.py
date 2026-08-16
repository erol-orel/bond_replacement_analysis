"""
Investable proxy total-return series (monthly, CHF) for the bond-replacement menu,
back to 2008, aligned to the Bloomberg constituent panel.

Broad menu (7 instruments, all with real, investable histories to <=2009):
  gold            SPDR Gold (GLD)                 real asset   USD -> CHF unhedged
  commodities     Invesco DB Commodity (DBC)      real asset   USD -> CHF unhedged
  infrastructure  iShares Global Infra (IGF)      equity-like  USD -> CHF unhedged
  convertibles    SPDR Blmbg Convertibles (CWB)   hybrid       USD -> CHF unhedged (from 2009)
  high_yield      iShares iBoxx HY (HYG)          credit       USD -> CHF HEDGED
  em_debt         iShares JPM EM Bond (EMB)       credit       USD -> CHF HEDGED
  managed_futures Guggenheim Mgd Futures (RYMFX)  diversifier  USD -> CHF unhedged

Currency: real/equity-like assets are held UNHEDGED (spot USDCHF); fixed-income-like
replacements (HY, EM debt) are CHF-HEDGED consistent with VZ's rule that only bonds are
hedged (PM email). The hedge return = USD local total return + (r_CHF - r_USD)/12 monthly,
using the SNB and Fed policy-rate paths from rates_monthly.csv (a negative carry / hedge
cost when CHF rates sit below USD rates).

Cat bonds are intentionally omitted: no investable vehicle has a clean 2008 history.

Output: data/processed/alternatives_chf_monthly.csv   (month-end CHF TR levels, base 100)
Run:  python src/data_alternatives.py   (needs rates_monthly.csv from data_bloomberg.py)
"""
from __future__ import annotations
import os, time
import numpy as np
import pandas as pd
import requests

CA = "/root/.ccr/ca-bundle.crt"
os.environ.setdefault("REQUESTS_CA_BUNDLE", CA)
os.environ.setdefault("SSL_CERT_FILE", CA)
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")

UNHEDGED = {"gold": "GLD", "commodities": "DBC", "infrastructure": "IGF",
            "convertibles": "CWB", "managed_futures": "RYMFX"}
HEDGED = {"high_yield": "HYG", "em_debt": "EMB"}


def fetch_yahoo(ticker, tries=4):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?range=30y&interval=1mo&events=div,splits")
    for k in range(tries):
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            r.raise_for_status()
            res = r.json()["chart"]["result"][0]
            idx = pd.to_datetime(res["timestamp"], unit="s")
            adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose")
            close = adj if adj is not None else res["indicators"]["quote"][0]["close"]
            s = pd.Series(close, index=idx).dropna().sort_index()
            s = s[~s.index.duplicated(keep="last")]
            s.index = s.index + pd.offsets.MonthEnd(0)
            return s
        except Exception as e:
            if k == tries - 1:
                raise RuntimeError(f"yahoo {ticker}: {e}")
            time.sleep(2 ** k)


def main():
    rates = pd.read_csv(os.path.join(PROC, "rates_monthly.csv"),
                        index_col=0, parse_dates=True)
    usdchf = fetch_yahoo("CHF=X")                    # CHF per USD (spot)
    carry = (rates["snb"] - rates["fed"]) / 100.0 / 12.0   # monthly CHF-hedge carry

    out = {}
    for name, tk in UNHEDGED.items():
        px = fetch_yahoo(tk)
        fx = usdchf.reindex(px.index, method="ffill")
        chf = (px * fx).dropna()
        out[name] = chf
    for name, tk in HEDGED.items():
        px = fetch_yahoo(tk)
        loc = px.pct_change()                        # USD local total return
        c = carry.reindex(px.index, method="ffill").fillna(0)
        r = (loc + c).dropna()
        lvl = (1 + r).cumprod()
        out[name] = lvl

    df = pd.DataFrame({k: v / v.dropna().iloc[0] * 100 for k, v in out.items()})
    df = df.loc["2008-01-31":"2026-06-30"]
    df.to_csv(os.path.join(PROC, "alternatives_chf_monthly.csv"))

    pd.set_option("display.width", 200)
    r = df.pct_change()
    ann = pd.DataFrame({
        "start": [df[c].first_valid_index().date() for c in df.columns],
        "CAGR%": [((df[c].dropna().iloc[-1] / df[c].dropna().iloc[0])
                   ** (1 / (df[c].dropna().shape[0] / 12)) - 1) * 100 for c in df.columns],
        "Vol%": r.std().values * np.sqrt(12) * 100,
        "n": r.count().values,
    }, index=df.columns)
    print("ALTERNATIVES (monthly CHF TR):", df.shape)
    print(ann.round(2).to_string())


if __name__ == "__main__":
    main()
