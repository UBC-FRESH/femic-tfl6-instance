# TFL 6 point-cloud bundle

The original TFL 6 product bundle carries DEM, DSM, slope, CHM, and canopy
rasters. It did not materialize the LidarBC point-cloud product. This directory
records the public point-cloud selection and product plan so the structure
habitat pilot can be rebuilt reproducibly.

## Source

- LidarBC point-cloud index, FeatureServer layer 4.
- AOI: `881700,627500,882700,628500` in EPSG:3005.
- Two OP24BMRS001 2024 LAZ tiles, 8 points/m², UTM zone 9 (EPSG:3156),
  CGVD2013, OGL-BC.
- The LAZ files are large and stay under `runtime/pointcloud/`; they are not
  committed.

## Rebuild

```bash
cd femic/external/femic-tfl6-instance

# Download the two public LAZ tiles into runtime/pointcloud/ using the URLs in
# config/lidar/tfl6_pointcloud_selection.json.

femic lidar bundle \
  --selection-manifest config/lidar/tfl6_pointcloud_selection.json \
  --product-plan config/lidar/tfl6_pointcloud_product_plan.json \
  --output-dir runtime/pointcloud/bundle \
  --overwrite \
  --generated-utc 2026-10-27T00:00:00+00:00

femic lidar validate --bundle runtime/pointcloud/bundle
```

The generated bundle has `bundle_version = 2026.10.0-tfl6-pointcloud`, two
`point_cloud` products, and per-product `EPSG:3156` CRS records. The bundle
manifest and LAZ bytes stay in `runtime/` and are not versioned.

## Structure consumer

`ws4` consumes the point-cloud bundle for the first-return structure metrics.
The resulting real TFL 6 pilot is in
`ws4/examples/structure_habitat_tfl6/`; it is not copied into this instance.
