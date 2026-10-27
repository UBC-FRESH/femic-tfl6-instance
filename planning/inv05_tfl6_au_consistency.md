# INV-05 TFL 6 species/AU consistency

Date: 2026-10-27
Script: `scripts/check_species_au_consistency.py`
Outputs:

- `planning/inv05_tfl6_au_consistency.csv`
- `planning/inv05_tfl6_au_consistency.json`

## Result

The TFL 6 AU review already carries a `species_combo`. The script derives the
top-two species combo from the VRI percentage columns and compares it with that
combo.

- Seven VRI blocks.
- Six comparable blocks: **6/6 species combos match** (100%).
- One block (`23339462`) has no VRI species rows and no AU row; it is reported as
  missing, not assigned a default.
- No AU or curve assignment changed.

Examples:

| Block | VRI top-two | AU combo |
| --- | --- | --- |
| 23339490 | CW+YC | CW+YC |
| 16625195 | YC+CW | YC+CW |
| 16624698 | HW+YC | HW+YC |

The VRI fractions for all six blocks are mixed; leading fractions range
0.40-0.60 and non-leading fractions 0.40-0.60.

## Interpretation

The current TFL 6 AU mapping already consumes VRI species composition, so the
new fraction contract agrees with it. The NTEMS dominant layer's disagreement
with VRI (4/6 leading species) does not change AU assignment; it is a separate
public-layer comparison.

This is a consistency check, not a new AU model. It does not alter curves,
growth, or the objective.

## Command

```bash
python scripts/check_species_au_consistency.py
```
