"""
Master analysis for the reframed thesis (2008-2026, monthly, CHF, net of fees):
replace the AP5 bond sleeve with a diversified basket of investable alternatives over the
WHOLE period, and study behaviour ACROSS four SNB rate regimes (not only low-rate windows).

Pipeline
  1. Load the monthly panel; define the real VZ AP5 strategic target and the replacement
     books (bond sleeve replaced by 0 / 33 / 66 / 100 %).
  2. Backtest every book with VZ Smart Rebalancing (monthly monitoring, +-20% bands),
     net of the agreed fee load (0.12% product + 1.25% management = 1.37% / yr).
  3. VALIDATE the reconstructed AP5 against the real VZ AP5 track record (2019-2026).
  4. Descriptive statistics + correlations (incl. the Swiss-vs-world-bond redundancy test).
  5. Regime tables: performance / risk of each book in each SNB regime, and the bond
     sleeve's own behaviour by regime (low-rate vs rising-rate).
  6. Figures + CSV tables to analysis/ and reports/figures/.

Run:  python src/analysis_2008.py   (after build_panel.py)
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import openpyxl
from engine import backtest, perf_metrics

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
ANL = os.path.join(HERE, "analysis")
FIG = os.path.join(HERE, "reports", "figures")
os.makedirs(ANL, exist_ok=True); os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 9, "axes.grid": True,
                     "grid.alpha": 0.3, "figure.autolayout": True})

FEE_ANNUAL = 0.0012 + 0.0125          # product + management (agreed with the director)
PER = 12                               # monthly

# --- real VZ AP5 strategic target (current VVIA allocation, Consolidation_allocations) ---
AP5 = {"world_equity": 0.2625, "swiss_equity": 0.25, "real_estate": 0.05,
       "world_bonds": 0.2395, "swiss_bonds": 0.168, "cash": 0.03}
BOND_SLEEVE = {"world_bonds": 0.2395, "swiss_bonds": 0.168}     # 40.75% total
BOND_TOTAL = sum(BOND_SLEEVE.values())
CORE = {k: v for k, v in AP5.items() if k not in BOND_SLEEVE}  # equity/RE/cash, fixed

# naive replacement basket: the 6 alternatives with full 2008 history, equal-weight
BASKET = ["gold", "commodities", "infrastructure", "managed_futures", "high_yield", "em_debt"]
BASKET_W = {k: 1.0 / len(BASKET) for k in BASKET}

# curated basket: drop the two money-losers (commodities, managed futures) and tilt to the
# defensive credit carry + a gold hedge that best fit a *bond* replacement
CURATED_W = {"high_yield": 0.35, "em_debt": 0.30, "gold": 0.20, "infrastructure": 0.15}

# four SNB rate regimes (Justification_sous_periodes_BNS.docx)
REGIMES = {
    "R1_2008-14_low_positive": ("2008-01-31", "2014-12-31"),
    "R2_2015-22_negative": ("2015-01-31", "2022-05-31"),
    "R3_2022-24_hikes_plateau": ("2022-06-30", "2024-02-29"),
    "R4_2024-26_easing": ("2024-03-31", "2026-06-30"),
    "Full_2008-26": ("2008-01-31", "2026-06-30"),
}


def replacement_book(frac: float, basket: dict = BASKET_W) -> dict:
    """AP5 with `frac` of the bond sleeve moved into `basket` (default = naive equal-weight)."""
    book = dict(CORE)
    for k, w in BOND_SLEEVE.items():
        book[k] = w * (1 - frac)
    for k, w in basket.items():
        book[k] = book.get(k, 0.0) + BOND_TOTAL * frac * w
    return {k: v for k, v in book.items() if v > 1e-9}


def load_vz_drift():
    """The real VZ AP5 target-allocation path (Consolidation_allocations.xlsx) as a
    target_schedule, used to tighten the validation reconstruction."""
    wb = openpyxl.load_workbook(os.path.join(HERE, "data", "bloomberg",
                                             "Consolidation_allocations.xlsx"), data_only=True)
    ws = wb.active
    sched = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        f = lambda x: float(x) if x is not None else 0.0
        book = {"world_equity": f(row[3]), "swiss_equity": f(row[4]), "real_estate": f(row[9]),
                "world_bonds": f(row[7]), "swiss_bonds": f(row[8]), "cash": f(row[10])}
        s = sum(book.values())
        if s <= 0:
            continue
        sched.append((pd.Timestamp(row[0]), {k: v / s for k, v in book.items()}))
    wb.close()
    return sched


def net_of_fee(value: pd.Series, fee_annual: float = FEE_ANNUAL) -> pd.Series:
    """Apply a constant fee load as a monthly drag on the value series."""
    r = value.pct_change().fillna(0.0)
    m = (1 + fee_annual) ** (1 / PER) - 1
    net = (1 + r - m).cumprod()
    return net / net.iloc[0] * 100


def run_books(px):
    books = {"P0_AP5_benchmark": AP5,
             "P1_replace_33": replacement_book(1 / 3),
             "P2_replace_66": replacement_book(2 / 3),
             "P3_replace_100": replacement_book(1.0)}
    gross, net, meta = {}, {}, {}
    for name, book in books.items():
        bt = backtest(px, book, mode="smart", rel_band=0.20, monitor_freq="ME", tc_bps=10)
        gross[name] = bt["value"]
        net[name] = net_of_fee(bt["value"])
        meta[name] = dict(n_rebal=bt["n_rebal"], turnover=round(bt["turnover"], 2))
    return books, gross, net, meta


# --------------------------------------------------------------------------- validation
def validate_vs_vz(px):
    vz = pd.read_csv(os.path.join(PROC, "vz_ap5_track_monthly.csv"),
                     index_col=0, parse_dates=True)["vz_ap5"]
    vz.index = vz.index.to_period("M").to_timestamp("M")
    # validate with VZ's REAL allocation drift (tighter than fixed weights); the 2008
    # backward extension still uses fixed strategic weights per the director.
    sched = load_vz_drift()
    bt = backtest(px, AP5, target_schedule=sched, mode="smart", rel_band=0.05,
                  monitor_freq="ME", tc_bps=10)
    recon = net_of_fee(bt["value"])
    # align to VZ window and rebase both to 100 at first common month
    common = recon.index.intersection(vz.index)
    common = common[common >= pd.Timestamp("2019-06-30")]
    r = recon.reindex(common); r = r / r.iloc[0] * 100
    v = vz.reindex(common); v = v / v.iloc[0] * 100
    rr, vr = r.pct_change().dropna(), v.pct_change().dropna()
    te = (rr - vr).std() * np.sqrt(PER)
    stats = dict(months=len(common),
                 recon_total=float(r.iloc[-1] / r.iloc[0] - 1),
                 vz_total=float(v.iloc[-1] / v.iloc[0] - 1),
                 corr=float(rr.corr(vr)),
                 tracking_error_ann=float(te),
                 mean_abs_month_gap=float((rr - vr).abs().mean()))
    return r, v, stats


# ------------------------------------------------------------------ descriptive stats
def descriptive_stats(px):
    rets = px.pct_change().dropna(how="all")
    rows = {}
    for c in px.columns:
        s = rets[c].dropna()
        lvl = px[c].dropna()
        dd = (lvl / lvl.cummax() - 1).min()
        rows[c] = dict(
            start=lvl.index.min().date(),
            CAGR=(lvl.iloc[-1] / lvl.iloc[0]) ** (PER / (len(lvl) - 1)) - 1,
            Vol=s.std() * np.sqrt(PER),
            Sharpe=(s.mean() * PER) / (s.std() * np.sqrt(PER)) if s.std() > 0 else np.nan,
            Skew=s.skew(), ExKurt=s.kurt(), MaxDD=dd)
    return pd.DataFrame(rows).T


def bond_redundancy(px):
    """Descriptive test of whether the two bond sub-indices can collapse to one index."""
    r = px[["swiss_bonds", "world_bonds"]].pct_change().dropna()
    corr = r["swiss_bonds"].corr(r["world_bonds"])
    return dict(corr_swiss_world_bonds=float(corr),
                swiss_vol=float(r["swiss_bonds"].std() * np.sqrt(PER)),
                world_vol=float(r["world_bonds"].std() * np.sqrt(PER)))


# ------------------------------------------------------------------------- regime tables
def regime_metrics(value_dict):
    out = {}
    for reg, (s, e) in REGIMES.items():
        rows = {}
        for name, v in value_dict.items():
            seg = v.loc[(v.index >= s) & (v.index <= e)]
            if len(seg) > 2:
                m = perf_metrics(seg, periods=PER)
                rows[name] = dict(CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"],
                                  MaxDD=m["MaxDD"])
        out[reg] = pd.DataFrame(rows).T
    return out


def bond_sleeve_by_regime(px):
    """Return of each bond sub-index (and cash) in each regime — the low-rate vs
    rising-rate commentary the director asked for."""
    rows = {}
    for reg, (s, e) in REGIMES.items():
        seg = px.loc[(px.index >= s) & (px.index <= e)]
        rows[reg] = {}
        for c in ["swiss_bonds", "world_bonds", "cash"]:
            sub = seg[c].dropna()
            n = len(sub) - 1
            rows[reg][c] = (sub.iloc[-1] / sub.iloc[0]) ** (PER / n) - 1 if n > 0 else np.nan
    return pd.DataFrame(rows).T


# ------------------------------------------------------------------------------- figures
def fig_cumulative(net):
    fig, ax = plt.subplots(figsize=(9.5, 5))
    for k, v in net.items():
        lw = 2.4 if k == "P0_AP5_benchmark" else 1.5
        ax.plot(v, label=k, lw=lw)
    for s, e in [REGIMES["R2_2015-22_negative"]]:
        ax.axvspan(pd.Timestamp(s), pd.Timestamp(e), color="grey", alpha=0.08)
    ax.set_title("Cumulative CHF total return, net of fees (2008-2026) — AP5 vs bond-replacement")
    ax.set_ylabel("Index (100 = 2008-01)"); ax.legend(fontsize=8)
    fig.savefig(os.path.join(FIG, "01_cumulative_2008.png")); plt.close(fig)


def fig_validation(r, v):
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(v, label="Real VZ AP5 (VVIA) track record", lw=2.4, color="black")
    ax.plot(r, label="Reconstructed AP5 (indices, Smart Reb., net of fees)", lw=1.6,
            ls="--", color="tab:red")
    ax.set_title("Validation: reconstructed AP5 vs real VZ track record (rebased 100, 2019-2026)")
    ax.set_ylabel("Index"); ax.legend(fontsize=8)
    fig.savefig(os.path.join(FIG, "02_ap5_validation.png")); plt.close(fig)


def fig_drawdown(net):
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    for k in ["P0_AP5_benchmark", "P3_replace_100"]:
        v = net[k]; dd = (v / v.cummax() - 1) * 100
        ax.plot(dd, label=k, lw=1.4)
    ax.set_title("Drawdown (%) — AP5 vs full bond-replacement"); ax.set_ylabel("Drawdown %")
    ax.legend(fontsize=8); fig.savefig(os.path.join(FIG, "03_drawdown_2008.png")); plt.close(fig)


def fig_regime_bars(reg_tables):
    regs = [k for k in REGIMES if k != "Full_2008-26"]
    books = ["P0_AP5_benchmark", "P3_replace_100"]
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    x = np.arange(len(regs)); w = 0.38
    for i, b in enumerate(books):
        vals = [reg_tables[r].loc[b, "CAGR"] * 100 if b in reg_tables[r].index else np.nan
                for r in regs]
        ax.bar(x + (i - 0.5) * w, vals, w, label=b)
    ax.set_xticks(x); ax.set_xticklabels([r.split("_", 1)[1] for r in regs], fontsize=7.5)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Annualised return %"); ax.set_title("Annualised return by SNB regime")
    ax.legend(fontsize=8); fig.savefig(os.path.join(FIG, "04_regime_returns.png")); plt.close(fig)


def fig_bonds_by_regime(bond_reg):
    regs = [k for k in REGIMES if k != "Full_2008-26"]
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    x = np.arange(len(regs)); w = 0.27
    for i, c in enumerate(["swiss_bonds", "world_bonds", "cash"]):
        vals = [bond_reg.loc[r, c] * 100 for r in regs]
        ax.bar(x + (i - 1) * w, vals, w, label=c)
    ax.set_xticks(x); ax.set_xticklabels([r.split("_", 1)[1] for r in regs], fontsize=7.5)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Annualised return %")
    ax.set_title("Bond sleeve behaviour by rate regime (the problem the thesis targets)")
    ax.legend(fontsize=8); fig.savefig(os.path.join(FIG, "05_bonds_by_regime.png")); plt.close(fig)


def fig_corr_heatmap(px):
    cols = ["swiss_bonds", "world_bonds", "swiss_equity", "world_equity", "real_estate",
            "gold", "commodities", "infrastructure", "managed_futures", "high_yield",
            "em_debt", "cash"]
    C = px[cols].pct_change().dropna().corr()
    fig, ax = plt.subplots(figsize=(8.2, 7))
    im = ax.imshow(C, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=90, fontsize=7)
    ax.set_yticks(range(len(cols))); ax.set_yticklabels(cols, fontsize=7)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{C.iloc[i,j]:.2f}", ha="center", va="center", fontsize=5.5)
    fig.colorbar(im, fraction=0.046); ax.set_title("Monthly return correlations (2008-2026)")
    fig.savefig(os.path.join(FIG, "06_correlation.png")); plt.close(fig)


def fig_rolling_corr(px):
    r = px[["swiss_equity", "world_equity", "swiss_bonds", "world_bonds"]].pct_change()
    eq = r[["swiss_equity", "world_equity"]].mean(axis=1)
    bd = r[["swiss_bonds", "world_bonds"]].mean(axis=1)
    rc = eq.rolling(24).corr(bd)
    fig, ax = plt.subplots(figsize=(9.5, 4))
    ax.plot(rc, lw=1.4)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvspan(pd.Timestamp("2022-06-30"), pd.Timestamp("2024-02-29"), color="red", alpha=0.1,
               label="2022-24 hikes")
    ax.set_title("Rolling 24m equity-bond correlation (diversification breaks down in 2022)")
    ax.set_ylabel("corr"); ax.legend(fontsize=8)
    fig.savefig(os.path.join(FIG, "07_rolling_corr.png")); plt.close(fig)


def run_curated(px):
    """Naive equal-weight basket vs the curated basket, at each replacement step."""
    net = {}
    for tag, basket in [("naive", BASKET_W), ("curated", CURATED_W)]:
        for frac in (1 / 3, 2 / 3, 1.0):
            bt = backtest(px, replacement_book(frac, basket), mode="smart", rel_band=0.20,
                          monitor_freq="ME", tc_bps=10)
            net[f"{tag}_{int(round(frac*100))}"] = net_of_fee(bt["value"])
    rows = {k: perf_metrics(v, periods=PER) for k, v in net.items()}
    tbl = pd.DataFrame(rows).T[["CAGR", "Vol", "Sharpe", "MaxDD", "CVaR95"]]
    return net, tbl


def fig_curated(net_books, curated_net):
    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.plot(net_books["P0_AP5_benchmark"], label="P0_AP5_benchmark", lw=2.4, color="black")
    ax.plot(net_books["P3_replace_100"], label="naive basket (100%)", lw=1.5, color="tab:orange")
    ax.plot(curated_net["curated_100"], label="curated basket (100%)", lw=1.8, color="tab:green")
    ax.set_title("Curated vs naive bond-replacement basket (100% replaced, net of fees)")
    ax.set_ylabel("Index (100 = 2008-01)"); ax.legend(fontsize=8)
    fig.savefig(os.path.join(FIG, "08_curated_vs_naive.png")); plt.close(fig)


def main():
    px = pd.read_csv(os.path.join(PROC, "panel_levels_monthly.csv"),
                     index_col=0, parse_dates=True)

    books, gross, net, meta = run_books(px)
    r, v, val = validate_vs_vz(px)
    desc = descriptive_stats(px)
    redun = bond_redundancy(px)
    reg_tables = regime_metrics(net)
    bond_reg = bond_sleeve_by_regime(px)
    curated_net, curated_tbl = run_curated(px)
    curated_tbl.to_csv(os.path.join(ANL, "curated_vs_naive.csv"))

    # full-period net metrics
    full = pd.DataFrame({k: perf_metrics(vv, periods=PER) for k, vv in net.items()}).T
    full = full[["CAGR", "Vol", "Sharpe", "Sortino", "MaxDD", "CVaR95", "Calmar"]]
    full.to_csv(os.path.join(ANL, "perf_full_net.csv"))
    desc.to_csv(os.path.join(ANL, "descriptive_stats.csv"))
    bond_reg.to_csv(os.path.join(ANL, "bond_sleeve_by_regime.csv"))
    for reg, tb in reg_tables.items():
        tb.to_csv(os.path.join(ANL, f"regime_{reg}.csv"))
    pd.DataFrame(books).T.fillna(0).to_csv(os.path.join(ANL, "book_weights.csv"))
    pd.Series(val).to_csv(os.path.join(ANL, "ap5_validation.csv"))

    # figures
    fig_cumulative(net); fig_validation(r, v); fig_drawdown(net)
    fig_regime_bars(reg_tables); fig_bonds_by_regime(bond_reg)
    fig_corr_heatmap(px); fig_rolling_corr(px)
    fig_curated(net, curated_net)

    pd.set_option("display.width", 220, "display.max_columns", 30)
    print("=== BOOK WEIGHTS ===")
    print(pd.DataFrame(books).T.fillna(0).round(3).to_string())
    print("\n=== FULL-PERIOD PERFORMANCE (net of fees, 2008-2026) ===")
    print((full * [100, 100, 1, 1, 100, 100, 1]).round(2).to_string())
    print("  meta:", meta)
    print("\n=== AP5 VALIDATION vs real VZ (2019-2026) ===")
    for k, x in val.items():
        print(f"   {k}: {x:.4f}" if isinstance(x, float) else f"   {k}: {x}")
    print("\n=== BOND SLEEVE BEHAVIOUR BY REGIME (ann. return %) ===")
    print((bond_reg * 100).round(2).to_string())
    print("   Swiss-vs-world bond monthly corr:", round(redun["corr_swiss_world_bonds"], 3))
    print("\n=== REGIME PERFORMANCE (net CAGR %, AP5 vs replacements) ===")
    for reg in REGIMES:
        t = reg_tables[reg]
        print(f"  [{reg}]  " + "  ".join(f"{b.split('_',1)[1] if '_' in b else b}={t.loc[b,'CAGR']*100:.1f}"
              for b in t.index))
    print("\n=== CURATED vs NAIVE BASKET (net of fees, full period) ===")
    print((curated_tbl * [100, 100, 1, 100, 100]).round(2).to_string())
    print("\nSaved analysis/*.csv and reports/figures/01-08_*.png")


if __name__ == "__main__":
    main()
