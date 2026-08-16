"""
Synthetic Insurance-Linked Securities (ILS / catastrophe-bond) total-return series.

There is no daily-liquid, long-history ILS ETF on Yahoo (the asset class trades in
monthly-subscription UCITS funds and OTC), so we build a transparent, reproducible
synthetic series calibrated to the realised behaviour of the Swiss Re Global Cat Bond
Total Return Index:

  return  = CHF risk-free (SNB path) + insurance risk premium (~4.5% p.a.)
  vol     = low day-to-day (~2-3% annualised) — premium accrues smoothly
  tails   = discrete catastrophe drawdowns (non-Gaussian left tail), e.g. Hurricane
            Ian (Sep 2022). Cat-bond indices posted record years in 2023 (~+20%) and
            2024 (~+17%) as spreads widened post-Ian — reproduced via the annual drift.

This is CLEARLY LABELLED synthetic. It exists so the covariance / crisis-hedge role of
ILS can be studied; it must NOT be read as a realised track record. See docs/methodology.md.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


# calendar-year total-return targets (%), calibrated to Swiss Re Cat Bond Index
_ANNUAL = {
    2019: 4.5, 2020: 5.8, 2021: 4.8, 2022: -2.0, 2023: 19.7,
    2024: 17.0, 2025: 9.5, 2026: 8.0,
}
# discrete catastrophe shocks: (date, cumulative drawdown over ~10 bdays)
_CAT_EVENTS = [
    ("2022-09-26", -0.115),   # Hurricane Ian
    ("2024-10-08", -0.030),   # Hurricane Milton (mild, mostly modelled-in)
]


def build_ils(index: pd.DatetimeIndex, snb_path) -> pd.Series:
    rng = np.random.default_rng(20240630)          # fixed seed -> reproducible
    idx = pd.DatetimeIndex(index)
    n = len(idx)

    # base drift: distribute each year's target return across its business days,
    # net of the injected catastrophe shocks so the year total still matches.
    daily_drift = np.zeros(n)
    for i, d in enumerate(idx):
        yr = d.year
        ann = _ANNUAL.get(yr, 6.0) / 100.0
        ndays = max((idx.year == yr).sum(), 1)
        daily_drift[i] = (1 + ann) ** (1 / ndays) - 1

    # smooth low-vol noise (~2.5% annualised)
    noise = rng.normal(0, 0.025 / np.sqrt(252), n)
    ret = daily_drift + noise

    # inject catastrophe drawdowns spread over 10 business days
    for date, dd in _CAT_EVENTS:
        loc = idx.searchsorted(pd.Timestamp(date))
        if 0 <= loc < n:
            span = slice(loc, min(loc + 10, n))
            k = len(range(*span.indices(n)))
            per = (1 + dd) ** (1 / k) - 1
            ret[span] += per

    lvl = 100 * (1 + pd.Series(ret, index=idx)).cumprod()
    return (lvl / lvl.iloc[0] * 100).rename("ils")
