from __future__ import annotations

from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
MIN_VOLUME = 1e-6


def _split_si_level(au_id: str) -> tuple[str, str]:
    parts = str(au_id).rsplit("_", 1)
    if len(parts) == 2 and parts[1].upper() in {"L", "M", "H"}:
        return parts[0], parts[1].upper()
    return str(au_id), ""


def _age_at_threshold(curve: pd.DataFrame, threshold: float) -> int | None:
    match = curve.loc[curve["volume"] >= threshold, "age"]
    if match.empty:
        return None
    return int(match.iloc[0])


def _count_material_sign_changes(diff: np.ndarray) -> int:
    material = diff[np.abs(diff) >= 0.25]
    if material.size < 2:
        return 0
    signs = np.sign(material)
    return int(np.sum(signs[1:] != signs[:-1]))


def _curve_shape_row(
    au_id: str, curve: pd.DataFrame, diag: pd.Series
) -> dict[str, object]:
    curve = curve.sort_values("age", kind="stable").reset_index(drop=True)
    age = curve["age"].to_numpy(dtype=float)
    volume = curve["volume"].to_numpy(dtype=float)
    diff = np.diff(volume)
    max_volume = float(np.nanmax(volume)) if volume.size else 0.0
    terminal_volume = float(volume[-1]) if volume.size else 0.0
    terminal_age = int(age[-1]) if age.size else 0
    peak_idx = int(np.nanargmax(volume)) if volume.size else 0
    peak_age = int(age[peak_idx]) if age.size else 0
    peak_volume = float(volume[peak_idx]) if volume.size else 0.0
    post_peak = volume[peak_idx:]
    post_peak_min = float(np.nanmin(post_peak)) if post_peak.size else peak_volume
    terminal_uptick_from_post_peak_min = terminal_volume - post_peak_min
    terminal_uptick_ratio = (
        terminal_uptick_from_post_peak_min / max(peak_volume, MIN_VOLUME)
        if peak_volume > 0
        else 0.0
    )
    last_20 = curve.loc[curve["age"] >= terminal_age - 20]
    last_50 = curve.loc[curve["age"] >= terminal_age - 50]
    last_20_gain = (
        float(last_20["volume"].iloc[-1] - last_20["volume"].iloc[0])
        if len(last_20) >= 2
        else 0.0
    )
    last_50_gain = (
        float(last_50["volume"].iloc[-1] - last_50["volume"].iloc[0])
        if len(last_50) >= 2
        else 0.0
    )
    max_single_year_drop = float(np.nanmin(diff)) if diff.size else 0.0
    max_single_year_gain = float(np.nanmax(diff)) if diff.size else 0.0
    negative_year_count = int(np.sum(diff < -0.25))
    large_negative_year_count = int(np.sum(diff < -5.0))
    sign_change_count = _count_material_sign_changes(diff)
    first_age_ge_1 = _age_at_threshold(curve, 1.0)
    first_age_ge_10 = _age_at_threshold(curve, 10.0)
    first_age_ge_50 = _age_at_threshold(curve, 50.0)
    volume_at_80 = float(np.interp(80.0, age, volume)) if volume.size else 0.0
    volume_at_120 = float(np.interp(120.0, age, volume)) if volume.size else 0.0
    volume_at_200 = float(np.interp(200.0, age, volume)) if volume.size else 0.0
    volume_at_250 = float(np.interp(250.0, age, volume)) if volume.size else 0.0
    base_au, si_level = _split_si_level(au_id)
    accepted = bool(diag.get("accepted", True))
    selected_path = str(diag.get("selected_path", ""))
    source_stand_count = int(diag.get("source_stand_count", 0))
    flags: list[str] = []
    severity = "ok"
    if not accepted:
        flags.append("not_accepted")
        severity = "insufficient_source"
    if accepted and first_age_ge_10 is not None and first_age_ge_10 >= 100:
        flags.append("late_start_ge10_after_age100")
        severity = "critical"
    if accepted and first_age_ge_50 is not None and first_age_ge_50 >= 160:
        flags.append("late_start_ge50_after_age160")
        severity = "critical"
    if accepted and volume_at_120 <= 1.0 and terminal_volume >= 25.0:
        flags.append("near_zero_to_old_age_then_jump")
        severity = "critical"
    if (
        accepted
        and terminal_uptick_from_post_peak_min >= 25.0
        and terminal_uptick_ratio >= 0.05
    ):
        flags.append("old_age_terminal_uptick")
        severity = "review" if severity == "ok" else severity
    if accepted and last_20_gain >= 20.0:
        flags.append("last_20_year_gain")
        severity = "review" if severity == "ok" else severity
    if accepted and last_50_gain >= 35.0:
        flags.append("last_50_year_gain")
        severity = "review" if severity == "ok" else severity
    if accepted and sign_change_count >= 4:
        flags.append("wobbly_multi_extrema")
        severity = "review" if severity == "ok" else severity
    if accepted and large_negative_year_count > 0:
        flags.append("large_single_year_drop")
        severity = "review" if severity == "ok" else severity
    recommendation = "accept_shape"
    if severity == "insufficient_source":
        recommendation = "borrow_or_fallback_required"
    elif (
        "near_zero_to_old_age_then_jump" in flags
        or "late_start_ge10_after_age100" in flags
    ):
        recommendation = "reject_current_fit_and_borrow_adjacent_au"
    elif (
        "old_age_terminal_uptick" in flags
        or "last_20_year_gain" in flags
        or "last_50_year_gain" in flags
    ):
        recommendation = "apply_tail_constraint_or_terminal_cap"
    elif "wobbly_multi_extrema" in flags or "large_single_year_drop" in flags:
        recommendation = "increase_smoothing_or_shape_constraint"
    return {
        "au_id": au_id,
        "base_au": base_au,
        "si_level": si_level,
        "accepted": accepted,
        "selected_path": selected_path,
        "source_stand_count": source_stand_count,
        "age_min": int(curve["age"].min()) if not curve.empty else None,
        "age_max": int(curve["age"].max()) if not curve.empty else None,
        "max_volume": round(max_volume, 6),
        "peak_age": peak_age,
        "peak_volume": round(peak_volume, 6),
        "terminal_volume": round(terminal_volume, 6),
        "first_age_ge_1": first_age_ge_1,
        "first_age_ge_10": first_age_ge_10,
        "first_age_ge_50": first_age_ge_50,
        "volume_at_80": round(volume_at_80, 6),
        "volume_at_120": round(volume_at_120, 6),
        "volume_at_200": round(volume_at_200, 6),
        "volume_at_250": round(volume_at_250, 6),
        "terminal_uptick_from_post_peak_min": round(
            terminal_uptick_from_post_peak_min, 6
        ),
        "terminal_uptick_ratio": round(terminal_uptick_ratio, 6),
        "last_20_gain": round(last_20_gain, 6),
        "last_50_gain": round(last_50_gain, 6),
        "max_single_year_drop": round(max_single_year_drop, 6),
        "max_single_year_gain": round(max_single_year_gain, 6),
        "negative_year_count": negative_year_count,
        "large_negative_year_count": large_negative_year_count,
        "sign_change_count": sign_change_count,
        "shape_severity": severity,
        "shape_flags": ";".join(flags),
        "recommended_action": recommendation,
    }


def _missing_curve_row(au_id: str, diag: pd.Series) -> dict[str, object]:
    base_au, si_level = _split_si_level(au_id)
    return {
        "au_id": au_id,
        "base_au": base_au,
        "si_level": si_level,
        "accepted": False,
        "selected_path": str(diag.get("selected_path", "insufficient_source_stands")),
        "source_stand_count": int(diag.get("source_stand_count", 0)),
        "age_min": int(diag.get("age_min", 0)),
        "age_max": int(diag.get("age_max", 0)),
        "max_volume": 0.0,
        "peak_age": 0,
        "peak_volume": 0.0,
        "terminal_volume": 0.0,
        "first_age_ge_1": None,
        "first_age_ge_10": None,
        "first_age_ge_50": None,
        "volume_at_80": 0.0,
        "volume_at_120": 0.0,
        "volume_at_200": 0.0,
        "volume_at_250": 0.0,
        "terminal_uptick_from_post_peak_min": 0.0,
        "terminal_uptick_ratio": 0.0,
        "last_20_gain": 0.0,
        "last_50_gain": 0.0,
        "max_single_year_drop": 0.0,
        "max_single_year_gain": 0.0,
        "negative_year_count": 0,
        "large_negative_year_count": 0,
        "sign_change_count": 0,
        "shape_severity": "insufficient_source",
        "shape_flags": "not_accepted",
        "recommended_action": "borrow_or_fallback_required",
    }


def _selected_au_ids() -> set[str]:
    static_au = pd.read_csv(INSTANCE_ROOT / "planning" / "tfl6_static_au_universe.csv")
    selected = static_au.loc[static_au["selected_top_90_stratum"].astype(bool), "au_id"]
    return set(selected.dropna().astype(str))


def _add_lmh_order_flags(summary: pd.DataFrame, curves: pd.DataFrame) -> pd.DataFrame:
    summary = summary.copy()
    summary["lmh_order_violation_count"] = 0
    summary["lmh_order_max_violation_m3ha"] = 0.0
    for base_au, group in curves.groupby("base_au", sort=True):
        levels = {
            level: table.set_index("age")["volume"].sort_index()
            for level, table in group.groupby("si_level")
            if level in {"L", "M", "H"}
        }
        violations: dict[str, float] = {}
        for low, high in (("L", "M"), ("M", "H"), ("L", "H")):
            if low not in levels or high not in levels:
                continue
            ages = levels[low].index.intersection(levels[high].index)
            if ages.empty:
                continue
            delta = levels[low].loc[ages].to_numpy() - levels[high].loc[ages].to_numpy()
            bad = delta > 5.0
            if np.any(bad):
                violations[f"{low}_gt_{high}"] = float(np.nanmax(delta[bad]))
        if not violations:
            continue
        mask = summary["base_au"] == base_au
        summary.loc[mask, "lmh_order_violation_count"] = len(violations)
        summary.loc[mask, "lmh_order_max_violation_m3ha"] = round(
            max(violations.values()), 6
        )
        review_mask = mask & (summary["shape_severity"] == "ok")
        summary.loc[review_mask, "shape_severity"] = "review"
        summary.loc[mask, "shape_flags"] = summary.loc[mask, "shape_flags"].map(
            lambda value: ";".join(
                item for item in [str(value).strip(";"), "lmh_order_violation"] if item
            )
        )
        summary.loc[review_mask, "recommended_action"] = "review_lmh_order_or_borrowing"
    return summary


def _write_markdown(summary: pd.DataFrame, output_path: Path) -> None:
    counts = Counter(summary["shape_severity"])
    flag_counts = Counter(
        flag
        for flags in summary["shape_flags"].fillna("")
        for flag in str(flags).split(";")
        if flag
    )
    action_counts = Counter(summary["recommended_action"])
    critical = summary.loc[summary["shape_severity"] == "critical"].copy()
    review = summary.loc[summary["shape_severity"] == "review"].copy()
    insufficient = summary.loc[
        summary["shape_severity"] == "insufficient_source"
    ].copy()
    top_columns = [
        "au_id",
        "source_stand_count",
        "shape_flags",
        "first_age_ge_10",
        "volume_at_120",
        "terminal_volume",
        "recommended_action",
    ]
    review_columns = [
        "au_id",
        "source_stand_count",
        "shape_flags",
        "terminal_uptick_from_post_peak_min",
        "last_20_gain",
        "sign_change_count",
        "recommended_action",
    ]
    lines = [
        "# TFL 6 First-Growth Curve Shape Diagnostics",
        "",
        "## Purpose",
        "",
        "Classify the current P3.4d natural/untreated first-growth curve shapes",
        "for the selected top-area AU set before changing smoothing parameters,",
        "borrowing rules, or Phase 4 bundle inputs. This report is diagnostic",
        "only: it does not alter",
        "`planning/tfl6_first_growth_au_curves.csv`.",
        "",
        "## Summary Counts",
        "",
        f"- Selected top-area AU diagnostic rows: `{len(summary)}`",
        f"- Accepted curve rows assessed: `{int(summary['accepted'].sum())}`",
        f"- OK shape rows: `{counts.get('ok', 0)}`",
        f"- Review shape rows: `{counts.get('review', 0)}`",
        f"- Critical shape rows: `{counts.get('critical', 0)}`",
        f"- Insufficient-source rows: `{counts.get('insufficient_source', 0)}`",
        "",
        "## Flag Counts",
        "",
    ]
    for flag, count in sorted(flag_counts.items()):
        lines.append(f"- `{flag}`: `{count}`")
    lines.extend(["", "## Recommended Action Counts", ""])
    for action, count in sorted(action_counts.items()):
        lines.append(f"- `{action}`: `{count}`")
    lines.extend(
        [
            "",
            "## Critical Cases",
            "",
            "Critical cases are accepted curves that appear unusable without a",
            "replacement rule, especially curves that stay effectively zero until",
            "old ages and then jump upward.",
            "",
        ]
    )
    if critical.empty:
        lines.append("No critical accepted-curve shape cases were flagged.")
    else:
        lines.append(critical[top_columns].to_markdown(index=False))
    lines.extend(
        [
            "",
            "## Review Cases",
            "",
            "Review cases are softer warnings: terminal upticks, wobbly multi-extrema",
            "behavior, large one-year drops, or L/M/H ordering violations.",
            "",
        ]
    )
    if review.empty:
        lines.append("No review-level accepted-curve shape cases were flagged.")
    else:
        lines.append(
            review.sort_values(
                [
                    "terminal_uptick_from_post_peak_min",
                    "last_20_gain",
                    "sign_change_count",
                ],
                ascending=[False, False, False],
            )
            .head(60)[review_columns]
            .to_markdown(index=False)
        )
        if len(review) > 60:
            lines.append("")
            lines.append(
                f"Only the first `60` review rows are shown here; see CSV for all `{len(review)}`."
            )
    lines.extend(
        [
            "",
            "## Insufficient-Source Cases",
            "",
            f"`{len(insufficient)}` selected top-area AUs still require borrowing/fallback review.",
            "",
            "## Parameter-Tuning Implications",
            "",
            "- Curves with `near_zero_to_old_age_then_jump` should not be accepted from",
            "  the current fit. Prefer borrowing from an adjacent SI class or similar",
            "  base AU until a support threshold or source-filter problem is resolved.",
            "- Curves with `old_age_terminal_uptick`, `last_20_year_gain`, or",
            "  `last_50_year_gain` need a tail constraint. Candidate tweaks include a",
            "  no-upturn-after-terminal-decline rule, a terminal cap after the last",
            "  reliable observed age bin, or a stronger old-age tail penalty.",
            "- Curves with `wobbly_multi_extrema` or `large_single_year_drop` need",
            "  stronger smoothing or a shape-constrained post-process before they are",
            "  eligible for model-input bundle use.",
            "- L/M/H order violations should be reviewed at the base-AU family level.",
            "  If the low or medium SI curve crosses a higher SI curve materially,",
            "  either borrow from the better-supported adjacent SI class or apply a",
            "  family-level ordering constraint.",
            "",
            "## Artifacts",
            "",
            "- `planning/tfl6_first_growth_shape_diagnostics.csv`",
            "- `planning/tfl6_first_growth_shape_diagnostics.md`",
            "- Non-selected AU imputation is audited separately in",
            "  `planning/tfl6_first_growth_au_remap_audit.csv`.",
            "- Inputs: `planning/tfl6_first_growth_au_curves.csv` and",
            "  `planning/tfl6_first_growth_au_fit_diagnostics.csv`",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    curves = pd.read_csv(INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_curves.csv")
    diagnostics = pd.read_csv(
        INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_fit_diagnostics.csv"
    )
    selected_au_ids = _selected_au_ids()
    curves = curves.loc[curves["au_id"].astype(str).isin(selected_au_ids)].copy()
    diagnostics = diagnostics.loc[
        diagnostics["au_id"].astype(str).isin(selected_au_ids)
    ].copy()
    diag_lookup = diagnostics.set_index("au_id", drop=False)
    rows = []
    curved_au_ids: set[str] = set()
    for au_id, curve in curves.groupby("au_id", sort=True):
        diag = (
            diag_lookup.loc[str(au_id)]
            if str(au_id) in diag_lookup.index
            else pd.Series()
        )
        rows.append(_curve_shape_row(str(au_id), curve, diag))
        curved_au_ids.add(str(au_id))
    for au_id, diag in (
        diagnostics.loc[~diagnostics["accepted"].astype(bool)]
        .set_index("au_id", drop=False)
        .iterrows()
    ):
        if str(au_id) not in curved_au_ids:
            rows.append(_missing_curve_row(str(au_id), diag))
    summary = pd.DataFrame(rows).sort_values(["shape_severity", "base_au", "au_id"])
    accepted_curves = curves.merge(
        summary[["au_id", "base_au", "si_level", "accepted"]],
        on="au_id",
        how="inner",
    )
    accepted_curves = accepted_curves.loc[accepted_curves["accepted"]].copy()
    summary = _add_lmh_order_flags(summary, accepted_curves)
    severity_order = {"critical": 0, "review": 1, "insufficient_source": 2, "ok": 3}
    summary["severity_sort"] = summary["shape_severity"].map(severity_order).fillna(9)
    summary = summary.sort_values(
        [
            "severity_sort",
            "recommended_action",
            "base_au",
            "si_level",
            "au_id",
        ],
        kind="stable",
    ).drop(columns=["severity_sort"])
    summary.to_csv(
        INSTANCE_ROOT / "planning" / "tfl6_first_growth_shape_diagnostics.csv",
        index=False,
    )
    _write_markdown(
        summary,
        INSTANCE_ROOT / "planning" / "tfl6_first_growth_shape_diagnostics.md",
    )
    counts = summary["shape_severity"].value_counts().to_dict()
    print(counts)


if __name__ == "__main__":
    main()
