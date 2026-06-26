from __future__ import annotations

from pathlib import Path
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]


def _plot_token(value: str) -> str:
    token = str(value).strip().lower()
    token = re.sub(r"[^a-z0-9_+.-]+", "_", token)
    return token.strip("_")


def _split_si_level(au_id: str) -> tuple[str, str]:
    parts = str(au_id).rsplit("_", 1)
    if len(parts) == 2 and parts[1].upper() in {"L", "M", "H"}:
        return parts[0], parts[1].upper()
    return str(au_id), ""


def _build_fitdiag_summary(raw_subset: pd.DataFrame) -> pd.DataFrame:
    table = raw_subset.rename(
        columns={"PRJ_TOTAL_AGE": "Age", "PRJ_VOL_DWB": "Vdwb"}
    ).copy()
    table["Age"] = pd.to_numeric(table["Age"], errors="coerce")
    table["Vdwb"] = pd.to_numeric(table["Vdwb"], errors="coerce")
    table = table.dropna(subset=["Age", "Vdwb"])
    table = table.loc[
        (table["Age"] >= 30) & (table["Age"] <= 350) & (table["Vdwb"] >= 0)
    ]
    if table.empty:
        return pd.DataFrame(columns=["age_bin", "median_volume", "p25", "p75"])
    table["age_bin"] = (np.floor(table["Age"] / 5.0) * 5.0).astype(float)
    return (
        table.groupby("age_bin", as_index=False)
        .agg(
            median_volume=("Vdwb", "median"),
            p25=("Vdwb", lambda s: float(s.quantile(0.25))),
            p75=("Vdwb", lambda s: float(s.quantile(0.75))),
        )
        .sort_values("age_bin", kind="stable")
        .reset_index(drop=True)
    )


def _write_lmh_plots(
    *,
    curves: pd.DataFrame,
    diagnostics: pd.DataFrame,
    output_dir: Path,
) -> list[dict[str, object]]:
    accepted = diagnostics.loc[diagnostics["accepted"].astype(bool)].copy()
    accepted[["base_au", "si_level"]] = pd.DataFrame(
        accepted["au_id"].map(_split_si_level).tolist(), index=accepted.index
    )
    curves = curves.merge(
        accepted[["au_id", "base_au", "si_level", "source_stand_count"]],
        on="au_id",
        how="inner",
    )
    rows: list[dict[str, object]] = []
    colors = {"L": "tab:blue", "M": "tab:green", "H": "tab:red", "": "black"}
    for base_au, group in curves.groupby("base_au", sort=True):
        fig, ax = plt.subplots(1, 1, figsize=(8, 5))
        ymax = 1.0
        levels: list[str] = []
        support: dict[str, int] = {}
        for level in ("L", "M", "H", ""):
            curve = group.loc[group["si_level"] == level].copy()
            if curve.empty:
                continue
            curve = curve.sort_values("age", kind="stable")
            label = level or "base"
            ax.plot(
                curve["age"],
                curve["volume"],
                linewidth=2.0,
                color=colors[level],
                label=label,
            )
            ymax = max(ymax, float(curve["volume"].max()))
            levels.append(label)
            support[label] = int(curve["source_stand_count"].max())
        ax.set_title(f"VDYP L/M/H Comparison: {base_au}")
        ax.set_xlabel("Age")
        ax.set_ylabel("Volume (m3/ha)")
        ax.set_xlim(0, 300)
        ax.set_ylim(0, ymax * 1.05)
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8)
        fig.tight_layout()
        filename = f"vdyp_lmh_tfl6-{_plot_token(base_au)}.png"
        path = output_dir / filename
        fig.savefig(path, dpi=150)
        plt.close(fig)
        rows.append(
            {
                "plot_type": "vdyp_lmh",
                "base_au": base_au,
                "au_id": "",
                "levels": ",".join(levels),
                "source_stand_count": sum(support.values()),
                "path": path.relative_to(INSTANCE_ROOT).as_posix(),
            }
        )
    return rows


def _write_fitdiag_plots(
    *,
    curves: pd.DataFrame,
    diagnostics: pd.DataFrame,
    stand_to_au: pd.DataFrame,
    yields: pd.DataFrame,
    output_dir: Path,
) -> list[dict[str, object]]:
    accepted = diagnostics.loc[diagnostics["accepted"].astype(bool)].copy()
    assignment = stand_to_au[["feature_id", "au_id"]].copy()
    assignment["FEATURE_ID"] = pd.to_numeric(assignment["feature_id"], errors="coerce")
    assignment = assignment.dropna(subset=["FEATURE_ID"])
    assignment["FEATURE_ID"] = assignment["FEATURE_ID"].astype(int)
    yields = yields.merge(
        assignment[["FEATURE_ID", "au_id"]], on="FEATURE_ID", how="inner"
    )
    rows: list[dict[str, object]] = []
    for au_id, curve in curves.groupby("au_id", sort=True):
        diag_match = accepted.loc[accepted["au_id"] == str(au_id)]
        if diag_match.empty:
            continue
        diag = diag_match.iloc[0]
        raw_subset = yields.loc[yields["au_id"] == str(au_id)].copy()
        if raw_subset.empty:
            continue
        observed = _build_fitdiag_summary(raw_subset)
        curve = curve.sort_values("age", kind="stable")
        fig, (ax, ax_resid) = plt.subplots(
            2,
            1,
            figsize=(8, 8),
            sharex=True,
            gridspec_kw={"height_ratios": [3, 1]},
        )
        raw_ids = sorted(raw_subset["FEATURE_ID"].dropna().astype(int).unique())
        max_raw = 200
        if len(raw_ids) > max_raw:
            raw_ids = raw_ids[:max_raw]
        raw_label_used = False
        for _feature_id, raw_rows in raw_subset.loc[
            raw_subset["FEATURE_ID"].isin(raw_ids)
        ].groupby("FEATURE_ID", sort=True):
            raw = raw_rows.rename(
                columns={"PRJ_TOTAL_AGE": "Age", "PRJ_VOL_DWB": "Vdwb"}
            ).copy()
            raw = raw.dropna(subset=["Age", "Vdwb"])
            raw = raw.loc[(raw["Age"] >= 0) & (raw["Age"] <= 350) & (raw["Vdwb"] >= 0)]
            if raw.empty:
                continue
            ax.plot(
                raw["Age"],
                raw["Vdwb"],
                color="0.5",
                alpha=0.08,
                linewidth=0.4,
                label="Raw VDYP curves" if not raw_label_used else None,
                zorder=1,
            )
            raw_label_used = True
        if not observed.empty:
            ax.fill_between(
                observed["age_bin"],
                observed["p25"],
                observed["p75"],
                color="lightblue",
                alpha=0.35,
                label="Observed P25-P75 (5y bins)",
            )
            ax.scatter(
                observed["age_bin"],
                observed["median_volume"],
                s=14,
                color="tab:blue",
                label="Observed median (5y bins)",
            )
        ax.plot(
            curve["age"],
            curve["volume"],
            color="black",
            linewidth=2.2,
            label="Selected fit",
        )
        ax.set_title(f"VDYP Fit Diagnostic: {au_id}")
        ax.set_xlabel("Age")
        ax.set_ylabel("Volume (m3/ha)")
        ax.set_xlim(0, 300)
        ymax = max(
            float(curve["volume"].max()) * 1.05,
            float(observed["p75"].max()) * 1.15 if not observed.empty else 1.0,
            1.0,
        )
        ax.set_ylim(0, ymax)
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8)
        ax.text(
            0.01,
            0.99,
            "\n".join(
                [
                    f"rmse={float(diag['rmse']):.1f}",
                    f"mape={float(diag['mape']):.3f}",
                    f"tail_rmse={float(diag['tail_rmse']):.1f}",
                    f"stands={int(diag['source_stand_count'])}",
                ]
            ),
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=7,
            bbox={"facecolor": "white", "alpha": 0.75, "edgecolor": "none"},
        )
        if not observed.empty:
            predicted = np.interp(
                observed["age_bin"].to_numpy(dtype=float),
                curve["age"].to_numpy(dtype=float),
                curve["volume"].to_numpy(dtype=float),
            )
            residual = predicted - observed["median_volume"].to_numpy(dtype=float)
            ax_resid.axhline(0.0, color="black", linewidth=1.0, alpha=0.6)
            ax_resid.scatter(
                observed["age_bin"], residual, s=14, color="tab:gray", alpha=0.8
            )
            ax_resid.plot(
                observed["age_bin"],
                residual,
                color="tab:gray",
                linewidth=1.2,
                alpha=0.7,
            )
        ax_resid.set_ylabel("Residual")
        ax_resid.set_xlabel("Age")
        ax_resid.grid(alpha=0.25)
        fig.tight_layout()
        filename = f"vdyp_fitdiag_tfl6-{_plot_token(str(au_id))}.png"
        path = output_dir / filename
        fig.savefig(path, dpi=150)
        plt.close(fig)
        rows.append(
            {
                "plot_type": "vdyp_fitdiag",
                "base_au": _split_si_level(str(au_id))[0],
                "au_id": au_id,
                "levels": _split_si_level(str(au_id))[1],
                "source_stand_count": int(diag["source_stand_count"]),
                "path": path.relative_to(INSTANCE_ROOT).as_posix(),
            }
        )
    return rows


def _selected_au_ids() -> set[str]:
    static_au = pd.read_csv(INSTANCE_ROOT / "planning" / "tfl6_static_au_universe.csv")
    selected = static_au.loc[static_au["selected_top_90_stratum"].astype(bool), "au_id"]
    return set(selected.dropna().astype(str))


def main() -> None:
    plots_dir = INSTANCE_ROOT / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    curves = pd.read_csv(INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_curves.csv")
    diagnostics = pd.read_csv(
        INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_fit_diagnostics.csv"
    )
    selected_au_ids = _selected_au_ids()
    curves = curves.loc[curves["au_id"].astype(str).isin(selected_au_ids)].copy()
    diagnostics = diagnostics.loc[
        diagnostics["au_id"].astype(str).isin(selected_au_ids)
    ].copy()
    stand_to_au = pd.read_csv(
        INSTANCE_ROOT / "planning" / "tfl6_stand_to_au_review.csv",
        low_memory=False,
    )
    yields = pd.read_parquet(
        INSTANCE_ROOT
        / "runtime"
        / "derived"
        / "p3_4_aflb_vdyp_first_growth_run2"
        / "vdyp_yield_timeseries.parquet"
    )
    for old_plot in plots_dir.glob("vdyp_lmh_tfl6-*.png"):
        old_plot.unlink()
    for old_plot in plots_dir.glob("vdyp_fitdiag_tfl6-*.png"):
        old_plot.unlink()
    manifest_rows = []
    manifest_rows.extend(
        _write_lmh_plots(curves=curves, diagnostics=diagnostics, output_dir=plots_dir)
    )
    manifest_rows.extend(
        _write_fitdiag_plots(
            curves=curves,
            diagnostics=diagnostics,
            stand_to_au=stand_to_au,
            yields=yields,
            output_dir=plots_dir,
        )
    )
    manifest = pd.DataFrame(manifest_rows).sort_values(
        ["plot_type", "base_au", "au_id"], kind="stable"
    )
    manifest.to_csv(
        INSTANCE_ROOT / "planning" / "tfl6_first_growth_plot_manifest.csv", index=False
    )
    summary = [
        "# TFL 6 First-Growth Curve Plot Manifest",
        "",
        f"- Selected top-area AU curves: `{len(selected_au_ids)}`",
        f"- LMH comparison plots: `{int((manifest['plot_type'] == 'vdyp_lmh').sum())}`",
        f"- Fit diagnostic plots: `{int((manifest['plot_type'] == 'vdyp_fitdiag').sum())}`",
        "- Plot directory: `plots/`",
        "- Filename families: `vdyp_lmh_tfl6-*.png` and `vdyp_fitdiag_tfl6-*.png`",
        "",
        "Cardinality note: `vdyp_fitdiag_tfl6-*.png` is one diagnostic plot per",
        "selected top-area AU curve, while `vdyp_lmh_tfl6-*.png` is one",
        "comparison panel per selected base stratum / AU family. Non-selected",
        "AUs are not published as separate curve families; they are imputed onto",
        "the selected canonical AU set by the lexicographic remap audit.",
        "",
        "These follow the MKRF/TSA29 visual review convention: L/M/H comparison",
        "panels for AU families and fit-diagnostic panels with raw VDYP curves,",
        "5-year observed medians/interquartile bands, selected fit, and residuals.",
        "",
    ]
    (INSTANCE_ROOT / "planning" / "tfl6_first_growth_plot_manifest.md").write_text(
        "\n".join(summary), encoding="utf-8"
    )
    print(summary[2])
    print(summary[3])
    print(summary[4])


if __name__ == "__main__":
    main()
