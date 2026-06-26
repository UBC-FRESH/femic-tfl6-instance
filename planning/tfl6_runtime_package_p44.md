# TFL 6 P4.4 Runtime Package Build and QA

## Scope

P4.4 assembles and smokes the first runnable TFL 6 Patchworks package after
P4.2 ForestModel/XML export and P4.3 Matrix Builder track QA.

The active runtime package root is:

- `models/tfl6_patchworks_model/`

Generated `blocks/`, `tracks/`, and `patchworksLog.csv` remain ignored until
Phase 5 decides which runtime artifacts are tracked, annexed, published, or
regenerated.

## Accepted Inputs

- ForestModel XML: `output/patchworks_tfl6_validated/forestmodel.xml`
- Fragments: `output/patchworks_tfl6_validated/fragments/fragments.*`
- Tracks: `models/tfl6_patchworks_model/tracks/*.csv`
- Runtime config: `config/patchworks.runtime.windows.yaml`

P4.3 accepted Matrix Builder run:

- run id: `tfl6_p43_matrix_accounts_wait20`
- `protoaccounts.csv`: 211 rows
- `accounts.csv`: 211 rows
- generic `CC` product and harvested-volume account surfaces present

## P4.4a Block and Topology Build

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic patchworks build-blocks `
  --config config\patchworks.runtime.windows.yaml `
  --topology-radius 200
```

The command exceeded the initial 120 second agent tool timeout but continued in
the background and completed. The process was allowed to finish rather than
being killed mid-topology.

Validation:

| Artifact | Result |
| --- | --- |
| `blocks.shp` rows | 24,879 |
| CRS | EPSG:3005 |
| Geometry validity | all valid |
| Area | 191,168.566 ha |
| Columns | `FRAGMENT_I`, `BLOCK`, `AREA_HA`, `F_AGE`, `AU`, `IFM`, `ORIGIN`, `SILV_STATE`, `RETENTION`, `TSA`, `geometry` |
| `topology_blocks_200r.csv` rows | 170,759 |
| Topology columns | `BLOCK1`, `BLOCK2`, `DISTANCE`, `LENGTH` |

P4.4a is accepted.

## Remaining P4.4 Steps

P4.4b must add the launch surface:

- `models/tfl6_patchworks_model/analysis/base.pin`
- shared headless helper script
- target helper script for the first representative scenario smoke

P4.4c must run direct launch smoke:

- `femic patchworks preflight`
- `femic patchworks run-headless models/tfl6_patchworks_model/analysis/base.pin`
- inspect saved-stage artifacts rather than relying on command success only

P4.4d must run a representative scenario smoke:

- activate an appropriate generic managed-volume target surface;
- confirm target status / target summary are written; and
- confirm schedule evidence is non-empty if a scheduling scenario is claimed.

Phase 4 closeout remains blocked until P4.4c/P4.4d produce direct runtime
evidence.
