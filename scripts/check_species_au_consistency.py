#!/usr/bin/env python3
"""Check VRI species fractions against the TFL6 AU species combo.

The TFL6 AU review already carries a ``species_combo`` (for example ``CW+YC``).
This check derives the top-two species combo from the VRI percentage columns and
reports agreement, mismatches, and missing species rows. It does not change AU
assignment or curves.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

SPECIES_CODES = tuple(f"species_cd_{index}" for index in range(1, 7))
SPECIES_PCTS = tuple(f"species_pct_{index}" for index in range(1, 7))


def _top_two_combo(
    properties: dict[str, Any],
) -> tuple[str | None, float | None, float | None]:
    """Return the top-two species combo and leading/non-leading fractions."""
    pairs: list[tuple[str, float]] = []
    for code_column, pct_column in zip(SPECIES_CODES, SPECIES_PCTS, strict=True):
        code = properties.get(code_column)
        pct = properties.get(pct_column)
        if code in (None, "") or pct in (None, ""):
            continue
        pairs.append((str(code), float(pct)))
    if not pairs:
        return None, None, None
    pairs.sort(key=lambda item: item[1], reverse=True)
    total = sum(pct for _code, pct in pairs)
    if abs(total - 100.0) > 1.0:
        raise ValueError(f"species percentages sum to {total:g}, not 100")
    combo = "+".join(code for code, _pct in pairs[:2])
    leading = pairs[0][1] / 100.0
    return combo, leading, 1.0 - leading


def evaluate(
    vri_geojson: Path, au_review_csv: Path
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Evaluate VRI species combos against the AU review table.

    Parameters
    ----------
    vri_geojson : Path
        VRI polygon GeoJSON with ``feature_id`` and species columns.
    au_review_csv : Path
        TFL6 stand-to-AU review CSV.

    Returns
    -------
    tuple of (list of dict, dict)
        Per-block rows and a summary.
    """
    with vri_geojson.open(encoding="utf-8") as handle:
        vri = json.load(handle)
    with au_review_csv.open(newline="", encoding="utf-8") as handle:
        review = {int(row["feature_id"]): row for row in csv.DictReader(handle)}
    rows: list[dict[str, object]] = []
    for feature in vri.get("features", []):
        properties = feature.get("properties", {})
        feature_id = int(properties["feature_id"])
        combo, leading, non_leading = _top_two_combo(properties)
        au_row = review.get(feature_id)
        au_combo = None if au_row is None else au_row.get("species_combo")
        rows.append(
            {
                "feature_id": feature_id,
                "vri_species_combo": combo,
                "au_species_combo": au_combo,
                "match": bool(
                    combo is not None and au_combo is not None and combo == au_combo
                ),
                "leading_fraction": leading,
                "non_leading_fraction": non_leading,
                "au_present": au_row is not None,
            }
        )
    comparable = [row for row in rows if row["au_present"] and row["vri_species_combo"]]
    matches = sum(bool(row["match"]) for row in comparable)
    summary = {
        "blocks": len(rows),
        "comparable": len(comparable),
        "matches": matches,
        "agreement_pct": (100.0 * matches / len(comparable)) if comparable else None,
        "missing_au": sum(not bool(row["au_present"]) for row in rows),
        "missing_vri_species": sum(row["vri_species_combo"] is None for row in rows),
    }
    return rows, summary


def main() -> None:
    """Run the check and write CSV plus JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vri-geojson",
        type=Path,
        default=Path("runtime/dem/p79_7_canopy_pilot/vri_aoi.geojson"),
    )
    parser.add_argument(
        "--au-review",
        type=Path,
        default=Path("planning/tfl6_stand_to_au_review.csv"),
    )
    parser.add_argument(
        "--out", type=Path, default=Path("planning/inv05_tfl6_au_consistency.csv")
    )
    parser.add_argument(
        "--summary", type=Path, default=Path("planning/inv05_tfl6_au_consistency.json")
    )
    args = parser.parse_args()
    rows, summary = evaluate(args.vri_geojson, args.au_review)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    args.summary.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
