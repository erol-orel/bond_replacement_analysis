"""
Unit tests for the core engine and portfolio construction (audit #38).
Runnable with pytest, or standalone:  python tests/test_engine.py
"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from engine import backtest, perf_metrics
from config_main import AP5, PER, FEE_ANNUAL, STEPS
from analysis_2008 import replacement_book, net_of_fee


def _prices(n=60, seed=1, cols=None):
    cols = cols or list(AP5)
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2008-01-31", periods=n, freq="ME")
    rets = rng.normal(0.003, 0.02, size=(n, len(cols)))
    lvl = 100 * np.cumprod(1 + rets, axis=0)
    return pd.DataFrame(lvl, index=idx, columns=cols)


def test_weights_sum_to_one():
    for pct in STEPS:
        book = AP5 if pct == 0 else replacement_book(pct / 100)
        assert abs(sum(book.values()) - 1.0) < 1e-9, f"weights !=1 at {pct}%"


def test_no_rebalance_inside_band():
    # flat prices -> weights never drift -> zero rebalances after the initial set
    px = _prices()
    px.iloc[:] = 100.0                      # constant levels => zero returns
    bt = backtest(px, AP5, mode="smart", rel_band=0.20, monitor_freq="ME", tc_bps=10)
    assert bt["n_rebal"] == 0, f"unexpected rebalances on flat prices: {bt['n_rebal']}"


def test_rebalance_when_band_crossed():
    # two assets 50/50; one doubles quickly -> band must be crossed -> at least one rebalance
    idx = pd.date_range("2008-01-31", periods=12, freq="ME")
    px = pd.DataFrame({"a": np.linspace(100, 400, 12), "b": np.full(12, 100.0)}, index=idx)
    bt = backtest(px, {"a": 0.5, "b": 0.5}, mode="smart", rel_band=0.10,
                  monitor_freq="ME", tc_bps=10)
    assert bt["n_rebal"] >= 1, "band clearly crossed but no rebalance triggered"


def test_fee_is_exact_multiplicative():
    idx = pd.date_range("2008-01-31", periods=13, freq="ME")
    v = pd.Series(100.0 * 1.01 ** np.arange(13), index=idx)   # +1%/month gross
    net = net_of_fee(v)
    m = (1 + FEE_ANNUAL) ** (1 / PER) - 1
    expected = ((1 + v.pct_change().fillna(0)) / (1 + m)).cumprod()
    expected = expected / expected.iloc[0] * 100
    assert np.allclose(net.values, expected.values), "fee not applied as exact (1+r)/(1+m)"


def test_transaction_cost_equals_turnover():
    # exact: with one rebalance, wealth(tc)/wealth(0) must equal (1 - turnover*tc/1e4)
    idx = pd.date_range("2008-01-31", periods=3, freq="ME")
    px = pd.DataFrame({"a": [100, 200, 200.0], "b": [100, 100, 100.0]}, index=idx)
    tc = 25.0
    bt0 = backtest(px, {"a": 0.5, "b": 0.5}, mode="smart", rel_band=0.10, monitor_freq="ME", tc_bps=0)
    btc = backtest(px, {"a": 0.5, "b": 0.5}, mode="smart", rel_band=0.10, monitor_freq="ME", tc_bps=tc)
    assert btc["n_rebal"] == 1 and bt0["n_rebal"] == 1, "expected exactly one rebalance"
    turn = bt0["trades"]["turnover"].iloc[0]
    ratio = btc["value"].iloc[-1] / bt0["value"].iloc[-1]
    assert abs(ratio - (1 - turn * tc / 1e4)) < 1e-9, "transaction cost != turnover * tc"


def test_no_lookahead():
    # decisions up to time t must depend only on data up to t: two price paths identical up to
    # the split, wildly different after -> value series up to the split must be identical.
    cols = list(AP5)
    px1 = _prices(n=48, seed=3, cols=cols)
    px2 = px1.copy()
    split = 24
    px2.iloc[split:] = px2.iloc[split:] * np.linspace(1, 5, len(px2) - split)[:, None]  # future shock
    bt1 = backtest(px1, AP5, mode="smart", rel_band=0.2, monitor_freq="ME", tc_bps=10)
    bt2 = backtest(px2, AP5, mode="smart", rel_band=0.2, monitor_freq="ME", tc_bps=10)
    assert np.allclose(bt1["value"].iloc[:split].values, bt2["value"].iloc[:split].values), \
        "future prices changed the past VALUE path -> look-ahead"
    # the real object to protect: the allocation DECISIONS (weights) before the split
    assert np.allclose(bt1["weights"].iloc[:split].values, bt2["weights"].iloc[:split].values), \
        "future prices changed past WEIGHTS/rebalance decisions -> look-ahead"


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"\nAll {len(fns)} tests passed.")


if __name__ == "__main__":
    _run_all()
