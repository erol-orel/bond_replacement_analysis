"""
Block-bootstrap Monte-Carlo distributions.

The base analysis is a single historical path (2019-2026). To judge whether the
bond-replacement advantage is robust rather than a lucky draw, we resample the realised
daily returns with a STATIONARY BLOCK BOOTSTRAP (Politis-Romano 1994): blocks of
consecutive days are drawn (mean length ~L) and concatenated into synthetic 7-year paths.
Blocks preserve short-horizon autocorrelation and — because we resample whole rows across
all assets jointly — the cross-asset correlation structure (crucial for portfolios).

For each of N synthetic paths we evaluate every (constant-mix) portfolio and collect the
distribution of CAGR, volatility, Sharpe and max drawdown, then report percentiles and the
probability each replacement book beats the AP5 benchmark.

Constant-mix (daily-rebalanced) weights are used so a path maps to portfolio returns by a
simple matrix product — the standard approach for bootstrap distribution studies. Calendar/
regime-dependent books (P4/P5, walk-forward) are excluded because bootstrap shuffling
destroys their time alignment; only fixed-weight books are meaningful here.
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from optimize import optimise, cov_matrix
import portfolios as P

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANL = os.path.join(HERE, "analysis")
FIG = os.path.join(HERE, "reports", "figures")

CORE = {"swiss_equity": 0.25, "world_equity": 0.25, "real_estate": 0.05, "cash": 0.03}
SLEEVE = ["swiss_bonds", "world_bonds", "gold", "convertibles", "clo",
          "infrastructure", "managed_futures", "ils", "private_credit"]
CAPS = {"gold": (0, 0.08), "convertibles": (0, 0.05), "clo": (0, 0.15),
        "infrastructure": (0, 0.10), "managed_futures": (0, 0.08), "ils": (0, 0.05),
        "private_credit": (0, 0.03), "swiss_bonds": (0, 0.42), "world_bonds": (0, 0.42)}
ILLIQUID_CAP = [(["ils", "private_credit"], 0.05)]

N_PATHS = 3000
MEAN_BLOCK = 20          # ~1 trading month
SEED = 12345


def stationary_bootstrap_indices(T, n_paths, mean_block, rng):
    """(n_paths x T) integer index array via stationary bootstrap (geometric blocks)."""
    p = 1.0 / mean_block
    idx = np.empty((n_paths, T), dtype=np.int64)
    idx[:, 0] = rng.integers(0, T, size=n_paths)
    new_block = rng.random((n_paths, T)) < p
    steps = rng.integers(0, T, size=(n_paths, T))
    for t in range(1, T):
        cont = (idx[:, t - 1] + 1) % T
        idx[:, t] = np.where(new_block[:, t], steps[:, t], cont)
    return idx


def path_metrics(port_rets, periods=252):
    """CAGR, vol, Sharpe, MaxDD for a (T,) return path (rf=0)."""
    lvl = np.cumprod(1.0 + port_rets)
    T = len(port_rets)
    cagr = lvl[-1] ** (periods / T) - 1.0
    vol = port_rets.std(ddof=1) * np.sqrt(periods)
    sharpe = (port_rets.mean() * periods) / vol if vol > 0 else np.nan
    peak = np.maximum.accumulate(lvl)
    maxdd = (lvl / peak - 1.0).min()
    return cagr, vol, sharpe, maxdd


def build_books(rets):
    """Fixed-weight books to test: AP5 + P1/P2/P3 + O1/O2/O3 optimised (full sample)."""
    books = {
        "P0_AP5_benchmark": P.AP5,
        "P1_swiss->CLO": P.P1_swiss_clo,
        "P2_swiss->diversified": P.P2_swiss_diversified,
        "P3_draft_recommended": P.P3_draft_recommended,
    }
    cols = list(CORE) + SLEEVE
    R = rets[cols]; cov = cov_matrix(R)
    for obj, label in [("max_sharpe", "O1_max_sharpe"),
                       ("min_variance", "O2_min_variance"),
                       ("min_cvar", "O3_min_cvar")]:
        r = optimise(R, obj, fixed=CORE, bounds=CAPS, group_caps=ILLIQUID_CAP, cov=cov)
        books[label] = P._normbook({k: v for k, v in r["weights"].items() if v > 1e-4})
    return books


def main():
    rets = pd.read_csv(os.path.join(HERE, "data/processed/returns_daily.csv"),
                       index_col=0, parse_dates=True)
    assets = list(rets.columns)
    Rmat = rets.values
    T = len(rets)
    rng = np.random.default_rng(SEED)

    books = build_books(rets)
    W = np.array([[b[a] for a in assets] for b in books.values()]).T  # assets x books
    labels = list(books.keys())

    print(f"Bootstrap: N={N_PATHS} paths, T={T} days, mean block={MEAN_BLOCK}, "
          f"{len(labels)} books")

    idx = stationary_bootstrap_indices(T, N_PATHS, MEAN_BLOCK, rng)
    # storage: metric arrays (n_paths x n_books)
    n_b = len(labels)
    CAGR = np.empty((N_PATHS, n_b)); VOL = np.empty_like(CAGR)
    SHP = np.empty_like(CAGR); MDD = np.empty_like(CAGR)
    for i in range(N_PATHS):
        pr = Rmat[idx[i]] @ W        # (T x books)
        for j in range(n_b):
            CAGR[i, j], VOL[i, j], SHP[i, j], MDD[i, j] = path_metrics(pr[:, j])

    # ---- percentile tables ----
    def pctile_table(arr, name):
        df = pd.DataFrame(arr, columns=labels)
        q = df.quantile([0.05, 0.25, 0.5, 0.75, 0.95]).T
        q.columns = [f"{name}_p{int(x*100)}" for x in [0.05, 0.25, 0.5, 0.75, 0.95]]
        q[f"{name}_mean"] = df.mean().values
        return q

    summary = pd.concat([pctile_table(CAGR, "CAGR"), pctile_table(SHP, "Sharpe"),
                         pctile_table(MDD, "MaxDD"), pctile_table(VOL, "Vol")], axis=1)
    summary.to_csv(os.path.join(ANL, "montecarlo_summary.csv"))

    # ---- probability of beating the benchmark ----
    bench = labels.index("P0_AP5_benchmark")
    prob = {}
    for j, lab in enumerate(labels):
        prob[lab] = dict(
            P_Sharpe_gt_bench=float(np.mean(SHP[:, j] > SHP[:, bench])),
            P_CAGR_gt_bench=float(np.mean(CAGR[:, j] > CAGR[:, bench])),
            P_smaller_MaxDD=float(np.mean(MDD[:, j] > MDD[:, bench])),  # less negative
            median_Sharpe=float(np.median(SHP[:, j])),
            median_MaxDD=float(np.median(MDD[:, j])),
        )
    probdf = pd.DataFrame(prob).T
    probdf.to_csv(os.path.join(ANL, "montecarlo_prob_beat_benchmark.csv"))

    # ---- figures ----
    order = ["P0_AP5_benchmark", "P2_swiss->diversified", "P3_draft_recommended",
             "O1_max_sharpe", "O2_min_variance", "O3_min_cvar"]
    order = [o for o in order if o in labels]
    oj = [labels.index(o) for o in order]

    # Sharpe distribution (violin)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.violinplot([SHP[:, j] for j in oj], showmedians=True)
    ax.set_xticks(range(1, len(order) + 1)); ax.set_xticklabels(order, rotation=20, fontsize=7)
    ax.axhline(np.median(SHP[:, bench]), color="grey", ls="--", lw=1,
               label="benchmark median")
    ax.set_ylabel("Sharpe"); ax.set_title(
        f"Bootstrap distribution of Sharpe ({N_PATHS} paths)"); ax.legend(fontsize=7)
    fig.savefig(os.path.join(FIG, "10_mc_sharpe_violin.png")); plt.close(fig)

    # MaxDD distribution
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.violinplot([MDD[:, j] * 100 for j in oj], showmedians=True)
    ax.set_xticks(range(1, len(order) + 1)); ax.set_xticklabels(order, rotation=20, fontsize=7)
    ax.set_ylabel("Max drawdown %"); ax.set_title(
        f"Bootstrap distribution of max drawdown ({N_PATHS} paths)")
    fig.savefig(os.path.join(FIG, "11_mc_maxdd_violin.png")); plt.close(fig)

    # CAGR histograms benchmark vs P2 vs O3
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for lab, c in [("P0_AP5_benchmark", "tab:blue"),
                   ("P2_swiss->diversified", "tab:orange"),
                   ("O3_min_cvar", "tab:green")]:
        if lab in labels:
            ax.hist(CAGR[:, labels.index(lab)] * 100, bins=60, alpha=0.5,
                    label=lab, color=c, density=True)
    ax.set_xlabel("CAGR %"); ax.set_ylabel("density")
    ax.set_title("Bootstrap distribution of CAGR"); ax.legend(fontsize=8)
    fig.savefig(os.path.join(FIG, "12_mc_cagr_hist.png")); plt.close(fig)

    # ---- console ----
    pd.set_option("display.width", 220, "display.max_columns", 40)
    print("\n=== MC SUMMARY: Sharpe percentiles ===")
    print((summary[[c for c in summary.columns if c.startswith("Sharpe")]]).round(2).to_string())
    print("\n=== MC SUMMARY: MaxDD percentiles (%) ===")
    mdcols = [c for c in summary.columns if c.startswith("MaxDD")]
    print((summary[mdcols] * 100).round(1).to_string())
    print("\n=== PROBABILITY OF BEATING AP5 BENCHMARK ===")
    print(probdf.round(3).to_string())
    print("\nSaved analysis/montecarlo_*.csv and reports/figures/10-12_*.png")


if __name__ == "__main__":
    main()
