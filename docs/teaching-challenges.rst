Advanced Student Challenges
===========================

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
