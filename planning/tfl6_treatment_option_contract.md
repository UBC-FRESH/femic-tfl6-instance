# TFL 6 Treatment Option Contract

## Purpose

This note defines the Phase 3 treatment-option vocabulary for the first TFL 6
Patchworks teaching model. It is a design contract for P3.5 only. It does not
define state transitions, build model-input tables, generate ForestModel XML,
run Matrix Builder, or assemble a Patchworks runtime package.

P3.6 must consume this vocabulary when transition logic is designed. Treatment
semantics should not be redefined in the transition lane.

## Accepted Treatment Catalogue

| Treatment ID | Label | Status | Role |
| --- | --- | --- | --- |
| `grow` | Grow/no scheduled treatment | Accepted implicit state behavior | Represents stands that remain unscheduled in a period. This is a model state path, not a harvest action. |
| `clearcut_and_plant` | Clearcut and plant | Accepted base scheduled treatment | Primary timber-harvest treatment for eligible managed THLB stands. Harvest and planted regeneration are treated as one base action for the first model. |
| `commercial_thinning` | Commercial thinning | Group-gated scenario treatment | Eligible only inside the K3Z/NICF core block and future accepted NICF expansion blocks after response, residual-state, and product rules are reviewed. |
| `fertilization` | Fertilization | Group-gated scenario treatment | Eligible only inside the K3Z/NICF core block and future accepted NICF expansion blocks after response and yield-assumption separation rules are reviewed. |

The first whole-TFL 6 base model should stay deliberately small:
`clearcut_and_plant` is the only base scheduled treatment. CT and fertilization
are not TFL-wide base treatments. They are retained as NICF-focused scenario
options because they match the teaching objective of exploring community-forest
and expansion-area tradeoffs inside the larger WFP-managed TFL 6 context.
Pre-commercial thinning, cedar-specific treatments, and standalone NICF
expansion actions are not accepted base treatments.

## Eligibility Filters

`clearcut_and_plant` is eligible only where all of the following are true in
the future model-input bundle:

- the stand is inside the accepted TFL 6 AOI;
- the stand is in the active THLB after the reviewed Phase 2 netdown;
- the stand is assigned `managed` treatment eligibility;
- the stand is not in a full-retention, reserve, non-THLB, or otherwise
  unschedulable status;
- the stand passes the accepted operability/yarding/slope eligibility filter
  for the selected scenario;
- the stand has a valid static AU assignment and a usable yield curve;
- the stand has reached the minimum harvest-age / merchantability rule that
  P3.6 will define; and
- any group-level constraints for NICF core, expansion candidates, WFP
  remainder, cedar signals, visual quality, or other reporting groups allow
  the treatment in that scenario.

`grow` is available to all stands with a valid state and curve assignment. It
does not change treatment eligibility or curve provenance.

`commercial_thinning` and `fertilization` are eligible only where all of the
following are true:

- the stand is inside `nicf_k3z_core` or an accepted future NICF expansion
  candidate group;
- the stand is in active THLB and assigned `managed` treatment eligibility;
- the stand is not in a full-retention, reserve, non-THLB, or otherwise
  unschedulable status;
- the stand passes the accepted operability/yarding/slope eligibility filter
  for the selected scenario;
- the stand has a valid static AU assignment and a usable yield curve;
- the stand meets the treatment-specific age, merchantability, stocking, and
  residual-state requirements that P3.6 or a later reviewed treatment lane
  defines; and
- the relevant response curve, product, account, and transition rules have
  been reviewed before activation.

These gated scenario treatments should be unavailable in the WFP/TFL 6
remainder unless the maintainer explicitly broadens the scenario scope later.

## Curve and Eligibility Semantics

The treatment catalogue preserves FEMIC/Patchworks semantics:

- `managed` / `unmanaged` means treatment eligibility only;
- `natural` / `treated` means curve provenance only;
- a natural-origin stand can still be treatment eligible if it is in managed
  THLB;
- an unmanaged stand can still carry a treated-origin curve if the source
  history supports it; and
- retention, operability, cedar signals, NICF identity, and expansion status
  are stand/group/scenario attributes, not AU identity fields and not curve
  provenance fields.

The post-harvest default for `clearcut_and_plant` is planted regeneration using
the reviewed TFL 6 treated/managed BatchTIPSY curve lane. That does not mean
all `managed` stands are already `treated`; it only defines the curve lane
after a managed regeneration transition.

## Product Hooks

The first P4 model-input bundle should expose the product hooks needed for
basic scheduling and teaching reports:

- total merchantable volume;
- available species or species-group volume where supported by the accepted
  curve tables;
- cedar volume/reporting hooks where cedar signal design has accepted fields;
- optional log-grade or utility-pole hooks only after P3.1 cedar product design
  resolves their source fields and confidence level; and
- harvested area by treatment, AU, source group, and stakeholder/reporting
  group.

P3.5 does not assign product equations or Patchworks account names. It defines
the treatment-side requirements P4 must satisfy when tables/XML are generated.

## Account and Reporting Hooks

The base catalogue must support reporting by:

- whole TFL 6;
- THLB and non-THLB;
- managed and unmanaged treatment eligibility;
- natural and treated curve provenance;
- NICF/K3Z core area;
- NICF expansion candidates and rejected candidates;
- WFP/TFL 6 remainder;
- cedar signal classes; and
- operability or slope-proxy sensitivity classes.

Those hooks let student projects compare stakeholder perspectives while
keeping the whole-TFL base action simple. CT and fertilization are explicitly
NICF-focused scenario treatments, not WFP/TFL-wide defaults.

## Deferred Treatments

The following remain explicit deferred design items:

| Treatment | Reason deferred | Required before activation |
| --- | --- | --- |
| Pre-commercial thinning | Not needed for the first runnable base model and not yet linked to reviewed TFL 6 response curves. | Stand-age/stocking eligibility, response curve logic, and teaching scenario purpose. |
| Commercial thinning outside K3Z/NICF expansion groups | Not accepted for the whole TFL 6 base model. | Explicit maintainer decision to broaden CT beyond NICF-focused scenario areas. |
| Fertilization outside K3Z/NICF expansion groups | Not accepted for the whole TFL 6 base model. | Explicit maintainer decision to broaden fertilization beyond NICF-focused scenario areas. |
| Cedar retention or cedar-product treatments | Stakeholder relevant but belongs to the cedar design lane. | P3.1 cedar signal, product, cultural reserve, treatment, and reporting decisions. |
| NICF expansion scenario actions | Stakeholder relevant but belongs to embedded identity and scenario-design lanes. | P3.2 identity fields and later scenario/account/target design. |

Deferred treatment entries are not rejected forever. They are blocked from the
base catalogue until their eligibility, response, product, account, and
teaching-purpose contracts are explicit.

## P3.6 Handoff

P3.6 should define:

- initial state classes;
- minimum harvest-age or merchantability rules for `clearcut_and_plant`;
- transitions from eligible pre-harvest state to harvested/regenerated state;
- the planted-regeneration transition after `clearcut_and_plant`;
- CT and fertilization eligibility only inside `nicf_k3z_core` and accepted
  future NICF expansion candidate groups;
- how managed/unmanaged eligibility changes, if at all, after retention or
  scenario filters;
- how operability sensitivity moves stands in or out of treatment eligibility
  without redefining AUs; and
- where cedar and NICF expansion hook points enter state, account, and report
  logic without becoming base treatment semantics.

## Acceptance Checks

- No accepted treatment ID encodes AU identity, stand age at time 0, THLB
  status, operability class, cedar status, or NICF expansion status.
- No accepted treatment rule infers `managed = treated` or
  `unmanaged = natural`.
- The whole-TFL 6 base scheduled treatment set is limited to
  `clearcut_and_plant`.
- CT and fertilization are gated to K3Z/NICF core and accepted future NICF
  expansion groups unless explicitly broadened later.
- Every deferred treatment has a documented blocker or review need.
