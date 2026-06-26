Advanced Student Challenges
===========================

Multi-Perspective Scenario Tradeoffs
------------------------------------

The TFL 6 teaching instance should support student projects that explore
tensions among stakeholder perspectives rather than search for a single
universal objective. The current TFL 6 AOI is managed in a Western Forest
Products context, while the original K3Z/NICF teaching tenure is mostly an
external reference area under the current boundary. Future NICF expansion
candidates are expected to come from proximal or adjacent public forested land
outside the current TFL 6 AOI. NICF stakeholders may value cedar, cultural
cedar visibility, community-forest continuity, and expansion opportunities,
while WFP-facing perspectives will also care about fibre supply volume, product
value, delivered-cost proxies, and mill/supply-chain implications.

A good student project should therefore compare scenarios using multiple KPI
families. Useful examples include harvest flow, growing-stock change, product
mix or value proxies, delivered-cost or operability proxies, cedar availability
and reserve outcomes, community-forest expansion area, treatment opportunity,
retention geography, and impacts on the TFL 6 remainder. These KPIs are
proxies for things stakeholders may value; they are not claims that every
stakeholder values every metric equally. Expansion scenarios should report the
outside-AOI source lands separately from current-AOI TFL 6 area so students do
not mistake candidate expansion geography for part of the base TFL 6 landbase.

Scenario interpretation should make the tradeoff visible. For example, an
NICF-preferred cedar or expansion scenario may improve community-facing
outcomes while reducing whole-TFL harvest flow or increasing delivered-cost
pressure. That tension is part of the teaching value of the instance.

Strategic RMZ Spatial Replacement
---------------------------------

The base teaching lane treats ``tfl6_nd_180`` as an aspatial MP10 Table 16
stand-level-retention deduction. This is a practical fallback because the
current public discovery pass did not locate materializable strategic Resource
Management Zone polygons or EFZ/GMZ/SMZ attributes that can be clipped to the
accepted TFL 6 AOI.

A useful advanced student challenge is to replace that fallback with a
geometry-backed implementation:

1. Locate a credible source for the missing strategic Resource Management Zone
   polygons or equivalent EFZ/GMZ/SMZ attribution for the TFL 6 area.
2. Materialize and clip that source to the accepted TFL 6 AOI.
3. Overlay the strategic RMZ geometry with landscape-unit and BEC strata.
4. Undo the base-case aspatial ``tfl6_nd_180`` deduction.
5. Implement the MP10 Table 16 stand-level-retention deduction using the
   geometry-backed RMZ/LU/BEC strata.
6. Rebuild the model inputs and Patchworks package.
7. Re-run a small set of teaching scenarios and compare whether the spatial
   replacement changes harvest flow, treatment placement, reserve geography, or
   other key outputs.

This exercise should be treated as an enhancement or sensitivity analysis, not
as a prerequisite for the base teaching model. It is valuable precisely because
it asks whether a more spatially faithful implementation changes conclusions
enough to matter.
