# TFL 6 State-Transition Contract

## Purpose

This note defines the Phase 3 state-transition contract for the first TFL 6
Patchworks teaching model. P3.6a defines the state classes and semantic fields
that P3.6b transition rules must consume. It does not build the model-input
bundle, generate ForestModel XML, run Matrix Builder, or assemble a Patchworks
runtime package.

The governing treatment vocabulary is
`planning/tfl6_treatment_option_contract.md`. Transition logic must consume
that vocabulary without redefining treatment semantics.

## Core State Fields

The first model-input bundle should keep these state dimensions separate:

| Field | Meaning | Examples |
| --- | --- | --- |
| `IFM` | Treatment eligibility only. | `managed`, `unmanaged` |
| `ORIGIN` | Curve provenance only. | `natural`, `treated` |
| `SILV_STATE` | Silviculture / state-path label. | `baseline`, `cc_planted`, `ct_candidate`, `fert_candidate`, `retained` |
| `RETENTION` | Retention fraction or retention class. | numeric fraction or reviewed class |
| `HARVEST_SYSTEM` | Operational harvest-system class. | `ground_based`, `cable`, `heli` |
| `TFL6_GROUP` | Spatial/reporting group identity. | `nicf_k3z_core`, `nicf_expansion_candidate`, `wfp_tfl6_remainder` |

These fields are not AU identity fields. AUs remain static BEC/phase/species/SI
families. Treatment eligibility, origin, harvest system, retention, cedar
signals, and NICF/expansion groups are stand attributes or scenario/reporting
attributes.

## Required State Classes

| State ID | Field expression | Meaning | Treatment eligibility |
| --- | --- | --- | --- |
| `initial_managed_natural` | `IFM=managed`, `ORIGIN=natural`, `SILV_STATE=baseline` | Existing natural-origin stand in managed THLB. | Eligible for `clearcut_and_plant` when age/merchantability, operability, harvest system, retention, and group constraints pass. |
| `initial_managed_treated` | `IFM=managed`, `ORIGIN=treated`, `SILV_STATE=baseline` | Existing treated-origin stand in managed THLB. | Eligible for `clearcut_and_plant`; CT/fertilization only where K3Z/NICF group gates and future response rules pass. |
| `initial_unmanaged_natural` | `IFM=unmanaged`, `ORIGIN=natural`, `SILV_STATE=baseline` | Natural-origin stand outside treatment eligibility. | Not eligible for scheduled treatments. |
| `initial_unmanaged_treated` | `IFM=unmanaged`, `ORIGIN=treated`, `SILV_STATE=baseline` | Treated-origin stand outside treatment eligibility. | Not eligible for scheduled treatments, but keeps treated curve provenance if source history supports it. |
| `retained_unmanaged` | `IFM=unmanaged`, `SILV_STATE=retained` | Area moved or held outside scheduling by retention/reserve/non-THLB rules. | Not eligible for scheduled treatments. |
| `post_clearcut_planted` | `IFM=managed`, `ORIGIN=treated`, `SILV_STATE=cc_planted` | Post-`clearcut_and_plant` regenerated stand on the treated/managed curve lane. | Future eligibility depends on age/merchantability and scenario rules. |
| `ct_candidate` | `IFM=managed`, `SILV_STATE=ct_candidate` | Optional candidate state for NICF-focused CT scenario logic. | Only inside `nicf_k3z_core` or accepted future `nicf_expansion_candidate` groups after reviewed CT rules exist. |
| `fert_candidate` | `IFM=managed`, `SILV_STATE=fert_candidate` | Optional candidate state for NICF-focused fertilization scenario logic. | Only inside `nicf_k3z_core` or accepted future `nicf_expansion_candidate` groups after reviewed fertilization rules exist. |
| `deferred_special` | explicit reviewed value | Placeholder for future cedar or expansion special states. | Not schedulable until a later reviewed lane defines the treatment/transition semantics. |

The table defines stable state IDs for planning. Phase 4 may encode the same
contract with separate Patchworks track fields rather than one concatenated
state string, but the semantics must remain equivalent.

## Semantic Rules

- `managed` / `unmanaged` is treatment eligibility only.
- `natural` / `treated` is curve provenance only.
- `SILV_STATE` records the state path, not the AU identity.
- `HARVEST_SYSTEM` is a TFL-wide operational attribute, not an AU or curve
  identity.
- A natural-origin managed stand can be harvested and transition to a
  treated-origin planted state.
- An unmanaged stand may carry a treated-origin curve if source history
  supports it, but it remains unavailable for scheduled treatments.
- Retention, non-THLB, reserves, and scenario exclusions should move or hold
  area in an unmanaged/retained state without changing the static AU.
- Operability or slope sensitivity can change eligibility for scheduling, but
  should not alter AU identity or curve provenance.

## Harvest-System Boundary

P3.6b/P4 must carry `HARVEST_SYSTEM` throughout TFL 6 with these accepted
classes:

- `ground_based`;
- `cable`; and
- `heli`.

The field should be available for:

- `clearcut_and_plant` eligibility;
- CT/fertilization eligibility where those treatments are group-gated;
- delivered-cost and harvest-system proxy accounts;
- harvest volume and area reports by system;
- operability sensitivity runs; and
- student scenario comparisons.

The field should not create separate AU IDs or separate yield-curve families by
itself.

## P3.6b Transition Handoff

The next tranche should define transition rows for:

- `grow`: no scheduled action, state persists and age advances;
- `clearcut_and_plant`: eligible managed stand transitions to
  `post_clearcut_planted` and `ORIGIN=treated`;
- retained/non-THLB/reserve movement: eligible or ineligible source stands
  move or remain in `retained_unmanaged` / `IFM=unmanaged`;
- initial natural and treated origins: starting curve provenance is retained
  until a treatment transition explicitly changes it;
- operability sensitivity: changes treatment eligibility or scenario masks,
  not AU identity;
- CT/fertilization: optional transitions only inside `nicf_k3z_core` and
  accepted future `nicf_expansion_candidate` groups after reviewed response
  rules exist; and
- cedar and expansion hooks: fields are carried for future accounts/reports,
  but cedar/expansion treatment semantics remain deferred.

## Deferred Transition Semantics

| Deferred item | Blocker |
| --- | --- |
| CT residual-state transition | Needs reviewed age/volume eligibility, removal fraction, residual curve behavior, products, and accounts. |
| Fertilization response transition | Needs clear separation between TIPSY yield assumptions already embedded in curves and optional scheduled fertilization response logic. |
| Cedar-specific state transitions | Depends on P3.1 cedar product/cultural reserve/treatment design. |
| NICF expansion scenario transitions | Depends on P3.2 accepted expansion identity fields and later scenario design. |
| Harvest-system reassignment over time | Needs explicit scenario rule; base model treats harvest system as an initial stand-level operational attribute. |

## Acceptance Checks

- No state class redefines the P3.5 treatment vocabulary.
- No state class infers `managed = treated` or `unmanaged = natural`.
- State classes carry ground/cable/heli harvest systems as operational fields.
- State classes preserve static AU identity under age, operability, retention,
  and scenario changes.
- P3.6b can define transitions from this document without starting Phase 4
  model-input generation.
