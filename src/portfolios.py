"""
Portfolio definitions.

Universe (13 sleeves): the 6 AP5 sleeves + 7 bond-replacement candidates. Every portfolio
is expressed over the FULL universe (zeros where unused) so they can be compared on the
same footing and switched between regimes.

Design of the bond-replacement variants follows the mandate:
  1. Replace the SWISS bond sleeve first, during LOW-RATE periods.
  2. Then extend to the broader bond sleeve / add regime-robust diversifiers.

Low-rate regime = SNB policy rate <= +0.25% (from config.SNB_PATH). In-sample this gives
two low-rate windows (2019-07 -> 2022-09 and 2025-03 -> 2026-06) separated by the
2022-2025 tightening/normalisation.
"""
from __future__ import annotations
import pandas as pd
from config import AP5_TARGET, SNB_PATH

UNIVERSE = ["swiss_equity", "world_equity", "swiss_bonds", "world_bonds",
            "real_estate", "cash", "gold", "convertibles", "clo",
            "infrastructure", "managed_futures", "private_credit", "ils"]


def _full(d: dict) -> dict:
    """Expand a sparse weight dict to the full universe (zeros elsewhere); assert sum=1."""
    w = {k: 0.0 for k in UNIVERSE}
    w.update(d)
    s = sum(w.values())
    assert abs(s - 1.0) < 1e-6, f"weights sum to {s:.4f}, not 1: {d}"
    return w


# --------------------------------------------------------------------- static books
AP5 = _full(AP5_TARGET)                                     # P0 benchmark

# P1: replace the 16.8% Swiss bond sleeve entirely with AAA CLO (cleanest IG, liquid).
P1_swiss_clo = _full({**AP5_TARGET, "swiss_bonds": 0.0, "clo": 0.168})

# P2: replace the 16.8% Swiss bond sleeve with a diversified DEFENSIVE basket
#     (CLO 8.4 IG carry + ILS 4.2 pure diversifier + gold 4.2 crisis/inflation hedge).
P2_swiss_diversified = _full({**AP5_TARGET, "swiss_bonds": 0.0,
                              "clo": 0.084, "ils": 0.042, "gold": 0.042})

# P3: the LLM draft's recommended target — replace ~20 pts of the 42% bond sleeve with a
#     7-asset diversifying sleeve. Adapted to AP5's 16.8/25.2 split (bonds -> 8.4/13.8).
P3_draft_recommended = _full({
    "swiss_equity": 0.25, "world_equity": 0.25,
    "swiss_bonds": 0.084, "world_bonds": 0.138,      # 42% -> ~22.2% bonds
    "real_estate": 0.05, "cash": 0.03,
    "gold": 0.03, "clo": 0.05, "infrastructure": 0.05,
    "managed_futures": 0.028, "ils": 0.02, "convertibles": 0.01, "private_credit": 0.01,
})

STATIC_BOOKS = {
    "P0_AP5_benchmark": AP5,
    "P1_swiss_bonds->CLO": P1_swiss_clo,
    "P2_swiss_bonds->diversified": P2_swiss_diversified,
    "P3_draft_recommended": P3_draft_recommended,
}


# --------------------------------------------------------- regime (rates) switching
def low_rate_windows(threshold: float = 0.25):
    """Return list of (start, end, is_low) regime spans from the SNB path."""
    steps = [(pd.Timestamp(d), r) for d, r in SNB_PATH]
    spans = []
    for i, (d, r) in enumerate(steps):
        end = steps[i + 1][0] if i + 1 < len(steps) else pd.Timestamp("2100-01-01")
        spans.append((d, end, r <= threshold))
    # merge consecutive same-regime spans
    merged = []
    for s, e, low in spans:
        if merged and merged[-1][2] == low:
            merged[-1] = (merged[-1][0], e, low)
        else:
            merged.append((s, e, low))
    return merged


def regime_schedule(low_book: dict, normal_book: dict = AP5, threshold: float = 0.25):
    """Build a target_schedule: use low_book during low-rate windows, else normal_book."""
    sched = []
    for s, e, low in low_rate_windows(threshold):
        sched.append((s, low_book if low else normal_book))
    return sched


# P4: DYNAMIC — during low-rate windows, swap the Swiss bond sleeve for the diversified
#     defensive basket (P2 book); revert to AP5 when rates normalise. This is the literal
#     mandate: "replacement first on the swiss bond allocation during low-rate periods".
P4_schedule = regime_schedule(low_book=P2_swiss_diversified, normal_book=AP5)

# P5: DYNAMIC AGGRESSIVE — in low-rate windows replace the Swiss bond sleeve AND half the
#     world bond sleeve (12.6 pts) with a broader alternatives basket; revert to AP5 when
#     rates normalise.
P5_low_book = _full({
    "swiss_equity": 0.25, "world_equity": 0.25,
    "swiss_bonds": 0.0, "world_bonds": 0.126,
    "real_estate": 0.05, "cash": 0.03,
    "gold": 0.04, "clo": 0.10, "infrastructure": 0.06,
    "managed_futures": 0.04, "ils": 0.042, "convertibles": 0.012,
})
P5_schedule = regime_schedule(low_book=P5_low_book, normal_book=AP5)

DYNAMIC_BOOKS = {
    "P4_dynamic_swiss_replace": dict(target=AP5, target_schedule=P4_schedule),
    "P5_dynamic_broad_replace": dict(target=AP5, target_schedule=P5_schedule),
}
