"""Mark P10R MP11 managed curves as tentatively passed review."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REVIEW_STATUS = "tentatively_passed_review"
MODEL_INPUT_STATUS = "not_model_input"
DECISION_NOTE = (
    "Maintainer requested tentative review pass so P10R can proceed to updated "
    "VDYP curve generation and AU-wise TIPSY-vs-VDYP diagnostics. This does not "
    "promote curves to model-input status."
)

CURVE_CSV_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.csv"
CURVE_JSON_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.json"
COMPARISON_CSV_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.csv"
)
COMPARISON_JSON_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.json"
)
COMPARISON_MD_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.md"
)
PLOT_MANIFEST_CSV_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.csv"
)
PLOT_MANIFEST_JSON_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.json"
)
PLOT_MANIFEST_MD_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.md"
)


def _write_csv_with_review_status(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["review_status"] = REVIEW_STATUS
    df["model_input_status"] = MODEL_INPUT_STATUS
    df.to_csv(path, index=False)
    return df


def _write_json_rows(path: Path, row_key: str) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload[row_key]
    for row in rows:
        row["review_status"] = REVIEW_STATUS
        row["model_input_status"] = MODEL_INPUT_STATUS
    if "summary" in payload:
        payload["summary"]["review_status"] = REVIEW_STATUS
        payload["summary"]["review_decision_note"] = DECISION_NOTE
    else:
        payload["review_status_counts"] = {REVIEW_STATUS: len(rows)}
        payload["review_decision_note"] = DECISION_NOTE
    if path == PLOT_MANIFEST_JSON_PATH:
        payload["review_statuses"] = [REVIEW_STATUS]
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def _insert_or_replace_review_decision(path: Path, lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    start_marker = "## Review Decision"
    next_marker = "\n## "
    if start_marker in text:
        start = text.index(start_marker)
        next_start = text.find(next_marker, start + len(start_marker))
        if next_start == -1:
            text = text[:start].rstrip() + "\n\n" + "\n".join(lines) + "\n"
        else:
            text = (
                text[:start].rstrip()
                + "\n\n"
                + "\n".join(lines)
                + "\n"
                + text[next_start:]
            )
    else:
        insert_at = text.find("## Method")
        if insert_at == -1:
            insert_at = text.find("## Review Index")
        if insert_at == -1:
            text = text.rstrip() + "\n\n" + "\n".join(lines) + "\n"
        else:
            text = (
                text[:insert_at].rstrip()
                + "\n\n"
                + "\n".join(lines)
                + "\n\n"
                + text[insert_at:]
            )
    path.write_text(text, encoding="utf-8")


def _update_markdown() -> None:
    generated_at = datetime.now(UTC).isoformat(timespec="seconds")
    review_lines = [
        "## Review Decision",
        "",
        f"- Review status: `{REVIEW_STATUS}`",
        f"- Model-input status: `{MODEL_INPUT_STATUS}`",
        f"- Decision timestamp UTC: `{generated_at}`",
        f"- Decision note: {DECISION_NOTE}",
    ]
    _insert_or_replace_review_decision(COMPARISON_MD_PATH, review_lines)
    _insert_or_replace_review_decision(PLOT_MANIFEST_MD_PATH, review_lines)

    rebuild_text = (
        INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.md"
    ).read_text(encoding="utf-8")
    if "- Review status:" not in rebuild_text:
        rebuild_text = rebuild_text.replace(
            "- Parsed curve feature count: `27`\n",
            "- Parsed curve feature count: `27`\n"
            f"- Review status: `{REVIEW_STATUS}`\n"
            f"- Model-input status: `{MODEL_INPUT_STATUS}`\n",
        )
    else:
        rebuild_text = rebuild_text.replace(
            "- Review status: `p10r4e_comparison_review_required`",
            f"- Review status: `{REVIEW_STATUS}`",
        )
    rebuild_text = rebuild_text.replace(
        "The parsed curves are retained as review surfaces only; they are not "
        "model inputs and have not yet been compared against Phase 5 fallback "
        "curves.",
        "The parsed curves are retained as review surfaces only. They have been "
        "tentatively passed for P10R sequencing after Phase 5 fallback "
        "comparison and plot review, but they remain `not_model_input`.",
    )
    (INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.md").write_text(
        rebuild_text, encoding="utf-8"
    )


def main() -> None:
    curve_df = _write_csv_with_review_status(CURVE_CSV_PATH)
    comparison_df = _write_csv_with_review_status(COMPARISON_CSV_PATH)
    plot_df = _write_csv_with_review_status(PLOT_MANIFEST_CSV_PATH)

    _write_json_rows(CURVE_JSON_PATH, "rows")
    _write_json_rows(COMPARISON_JSON_PATH, "records")
    _write_json_rows(PLOT_MANIFEST_JSON_PATH, "records")
    _update_markdown()

    print(
        "Marked P10R MP11 managed curves as "
        f"{REVIEW_STATUS}: curve_rows={len(curve_df)}, "
        f"comparison_rows={len(comparison_df)}, plot_manifest_rows={len(plot_df)}"
    )


if __name__ == "__main__":
    main()
