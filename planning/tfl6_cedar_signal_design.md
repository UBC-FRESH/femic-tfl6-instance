# TFL 6 Cedar Signal Design

## Purpose

This note starts P3.1 by translating TFL 6 cedar evidence into model-design
requirements for the teaching instance.

Governing issue: `#8`.

This is a design note only. It does not generate model inputs, Patchworks XML,
Matrix Builder outputs, or a runtime package.

Related stakeholder framing is recorded in
`planning/tfl6_stakeholder_context.md`. Cedar design should make NICF/community
cedar interests visible while also reporting WFP-facing fibre supply, value,
and delivered-cost implications where the teaching model can support those
signals.

## Source Evidence

### Cultural Cedar Need

The 2012 AAC rationale records First Nations concerns about monumental and
old-growth cedar. KFN raised potential overharvest concerns, while MQFN and TFN
identified continued access to monumental cedar for cultural purposes. MQFN,
NFN, QFN, and TFN also raised archaeological-feature protection concerns.

The same rationale records WFP's position that a significant volume of
old-growth cedar exists in TFL 6, with a large portion outside the THLB, and
that non-contributing land may contain larger cedar trees suitable for canoes,
buildings, and poles. WFP also offered further engagement to discuss cultural
cedar needs and potential inventory of those needs.

Design implication: cultural cedar must not be represented only as harvested
volume. The model needs visible cedar availability and reserve/reporting
signals that can distinguish old/large cedar and non-THLB reserve context from
scheduled timber production.

Stakeholder implication: cedar reserve or cedar-priority scenarios should also
report consequences for whole-TFL and TFL 6 remainder fibre supply. The teaching
model should not imply that NICF-preferred cedar outcomes are costless to WFP
or to the broader TFL 6 fibre-supply system.

### Cedar Composition

The 2011 information package forest-cover summary records western redcedar as
the second-largest forest component after western hemlock:

- western hemlock: `102664 ha` / `67.5%`;
- western redcedar: `28608 ha` / `18.8%`; and
- yellow-cedar: `8212 ha` / `5.4%`.

Design implication: cedar is large enough to justify dedicated account/report
signals, but most forested area is not cedar-leading. The first design should
separate cedar-leading, cedar-present, yellow-cedar, and old/large cedar
signals rather than treating all conifer volume as equivalent.

### Productivity and Yield Evidence

The 2011 information package includes TFL 6-specific site-index conversion
evidence for Cw and other target species. Table 42 estimates Cw site index by
productivity group:

- PG1: `27.0 m`;
- PG2: `24.5 m`;
- PG3: `23.7 m`;
- PG2+3: `23.8 m`;
- PG4: `19.2 m`.

The AAC rationale records that fertilization effects for hemlock, spruce, and
redcedar were modeled using the next higher productivity group, with support
from Salal-Cedar-Hemlock Integrated Research Program work near Port McNeill.
It also records that genetically improved select seed was used for Douglas-fir,
western hemlock, western redcedar, and yellow-cedar plantations.

Design implication: cedar yield behavior belongs in model-design assumptions,
not in THLB netdown. The first model-input bundle should preserve enough cedar
species, productivity-group, site-index, managed-origin, and treatment
attribution to support later cedar-specific curve/account decisions.

### K3Z Carry-Forward Boundary

The K3Z template provides useful structural patterns but not accepted TFL 6
cedar semantics. Existing planning already rejects carrying forward K3Z product
or account targets as TFL 6 cedar logic.

Design implication: P3.1 may borrow the shape of K3Z-style account/product and
reporting surfaces, but cedar thresholds, treatments, products, and targets
must be TFL 6-specific or explicitly marked as teaching approximations.

## First Cedar Signal Set

The first P3.1 design lane should define these source-derived signals for later
model-input generation:

| Signal | First definition | Purpose | Status |
| --- | --- | --- | --- |
| `cedar_leading` | Primary species is western redcedar (`CW`) or yellow-cedar (`YC`) in the accepted R1/VDYP-derived species fields. | Separate cedar-dominant stands for reporting, products, and treatment review. | Accepted for P3.1b as a derived signal, not an AU key. |
| `western_redcedar_leading` | `species_cd_1 == CW`. | Preserve Cw-specific cultural and utility-pole signals. | Accepted for P3.1b as a derived signal. |
| `yellow_cedar_leading` | `species_cd_1 == YC`. | Keep yellow-cedar visible without conflating it with Cw cultural cedar. | Accepted for P3.1b as a derived signal. |
| `cedar_present` | Sum `species_pct_1..6` where the matching `species_cd_1..6` value is `CW` or `YC`; flag stands with cedar share `>= 20%`. | Catch mixed stands where cedar is not leading but may matter for products or culture. | Accepted for P3.1b as the first threshold. |
| `old_cedar` | `cedar_present` and either `est_age_spp1 >= 141` or `est_age_spp2 >= 141`. | Approximate old-growth cedar reporting where direct monumental cedar inventory is unavailable. | Accepted for P3.1b as the first age proxy. |
| `large_cedar_proxy` | Cedar-leading or cedar-present stand above reviewed diameter/height proxy thresholds if source fields are available. | Proxy for monumental/pole-quality candidates and cultural-cedar availability. | Unresolved; no accepted DBH or pole-grade threshold is locked in P3.1b. |
| `cedar_cultural_reserve_context` | Cedar signal intersecting non-THLB, retained, reserve, or otherwise unmanaged landbase context once Phase 4 assigns final `IFM`/retention fields. | Report likely cultural cedar availability outside scheduled timber production. | Accepted as a reporting/accounting context, not a new THLB exclusion. |
| `cedar_harvest_candidate` | Cedar signal inside accepted THLB and eligible managed area once Phase 4 assigns final `IFM=managed`. | Report where cedar supply may enter harvest scheduling. | Accepted as a reporting/accounting context; depends on Phase 4 bundle fields. |

## P3.1b Source-Field Lock

P3.1b locks cedar source fields against the accepted Phase 3 review surface
`planning/tfl6_stand_to_au_review.csv`. That surface was built from the current
TFL 6 R1 geometry plus VDYP7 primary-layer attribution and is already used by
the static AU and yield-curve work.

Accepted cedar source fields for the first model-input bundle are:

| Field family | Accepted fields | P3.1b use |
| --- | --- | --- |
| Stand key and area | `feature_id`, `map_id`, `polygon_id`, `area_ha` | carry cedar signals back to stands and report area by signal |
| BEC/reporting strata | `bec_group`, `bec_zone_code`, `bec_subzone`, `bec_variant`, `bec_phase` | report cedar by ecological context without changing AU identity |
| Species codes | `species_cd_1` through `species_cd_6` | identify `CW` and `YC` leading or component cedar |
| Species percentages | `species_pct_1` through `species_pct_6` | compute total cedar component share for `cedar_present` |
| Age proxy | `est_age_spp1`, `est_age_spp2` | compute first `old_cedar` proxy at `>= 141` years |
| Height/supporting proxy | `est_height_spp1`, `est_height_spp2` | carry for later large-cedar and utility-pole review, but do not lock thresholds yet |
| Treatment-eligibility support | `for_mgmt_land_base_ind`, later Phase 4 `IFM` fields | distinguish managed harvest candidates from reserve/unmanaged contexts |
| AU/yield support | `au_id`, `stratum_code`, `selected_top_90_stratum` | report cedar against accepted AU/yield surfaces without using cedar in AU identity |

Gross P3.1b diagnostics from `planning/tfl6_stand_to_au_review.csv`:

| Signal | Rows | Gross area |
| --- | ---: | ---: |
| `western_redcedar_leading` | `3868` | `27980.000 ha` |
| `yellow_cedar_leading` | `659` | `5446.870 ha` |
| `cedar_leading` | `4527` | `33426.800 ha` |
| `cedar_present >= 20%` | `8454` | `62963.700 ha` |
| `old_cedar` using `cedar_present >= 20%` and age `>= 141` | `3838` | `23058.300 ha` |
| `cedar_present >= 20%` inside selected top-90 strata | `7255` | `54734.200 ha` |

These are gross review-surface diagnostics, not final Patchworks account values.
Phase 4 must recompute them against the final model-input bundle after THLB,
`IFM`, retention, embedded NICF/K3Z identity, and any accepted expansion
candidate fields are carried into the bundle.

P3.1b explicitly does not lock:

- DBH or pole-grade thresholds for `large_cedar_proxy`;
- cedar-specific treatments or fertilization/CT response assumptions;
- cedar-specific yield-curve families beyond the existing AU/yield surfaces;
- cultural cedar as a new base THLB exclusion; or
- any AU identity changes based on cedar status.

## Cultural Reserve Design

The base teaching model should not create a new hidden THLB exclusion for
cultural cedar. Phase 2 already applies the MP10 cultural heritage resources
fallback as part of THLB netdown.

For P3.1, cultural cedar should be represented as:

- a reporting/accounting signal for old/large cedar context;
- a scenario constraint candidate that can limit or reserve portions of
  cedar-relevant managed area; and
- a discussion surface for students to compare timber value against cultural
  availability.

Accepted first behavior:

- no additional base-case THLB deduction;
- no automatic exclusion of all old cedar from harvest eligibility;
- report cedar availability both inside and outside THLB; and
- leave scenario-specific cedar reserve targets for later model-design review.

## Utility-Pole Product Design

Utility-pole-grade cedar should be treated as a product/reporting design lane,
not as a source-layer extraction step.

Minimum first-bundle requirements:

- cedar species signal;
- old/large proxy or explicit diameter/height fields if available;
- managed/unmanaged treatment eligibility;
- natural/treated curve provenance;
- cedar volume by analysis unit or curve group; and
- a product/account surface that can distinguish generic cedar volume from
  candidate high-value utility-pole potential.

Open review questions for P3.1c:

- Which diameter, height, age, or volume thresholds are defensible as a first
  utility-pole proxy?
- Should utility-pole potential be reported as a product, a feature/account, or
  both?
- Should the first base model constrain harvest of utility-pole candidates, or
  only report their scheduled and residual quantities?

## Treatment and Yield Implications

Treatment assumptions should stay separate from source extraction:

- fertilization response for redcedar was modeled historically through
  productivity-group uplift, but the first teaching model should not silently
  hard-code that as a new cedar treatment without review;
- genetically improved cedar stock is relevant for managed-origin curve
  assumptions, but managed-origin and treated-origin semantics must remain
  distinct; and
- cedar-specific treatment variants should be explicit scenario alternatives,
  not implicit edits to base THLB or source-layer status.

P3.1c should define whether the first bundle needs:

- cedar-specific products only;
- cedar-specific accounts/reports only;
- cedar-specific treatment eligibility;
- cedar-specific yield-curve groupings; or
- all of the above.

## Patchworks-Facing Requirements

The first model-input bundle should preserve enough fields to build these
Patchworks-facing surfaces later:

| Surface | Minimum requirement |
| --- | --- |
| Feature/account | Area by cedar-leading, Cw-leading, Cy-leading, cedar-present, old cedar, and cedar cultural reserve context. |
| Product | Generic harvested cedar volume plus a provisional utility-pole candidate product or reporting class if reviewed thresholds are available. |
| Target/report | Residual old/large cedar context, scheduled cedar volume, and cedar harvest versus reserve tradeoff reports. |
| Stakeholder comparison | NICF/K3Z cedar outcomes versus whole-TFL and WFP-facing fibre-supply/value/cost signals where available. |
| Treatment hook | Optional cedar-oriented treatment family, only after P3.1c accepts a teaching treatment design. |
| QA | Source species-area shares must be compared against MP10 forest-cover shares before accepting the first bundle. |

## P3.1a Decision Boundary

P3.1a accepts only the evidence base and first design questions. It does not
lock source fields, thresholds, products, targets, or treatments.

P3.1b accepts the first source fields and derived signals above. P3.1c should
turn the accepted signals into explicit Patchworks-facing product, account,
treatment-hook, stakeholder-comparison, and report requirements.
