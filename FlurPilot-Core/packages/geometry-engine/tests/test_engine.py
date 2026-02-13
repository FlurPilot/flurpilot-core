"""Smoke tests for Geometry Engine Python bindings."""

import pytest


def test_geometry_engine_import():
    """Test that the geometry engine can be imported."""
    from geometry_engine import calculate_virtual_parcel, version
    assert version is not None


def test_virtual_parcel_calculation():
    """Test basic virtual parcel calculation."""
    import json
    from geometry_engine import calculate_virtual_parcel

    request = {
        "field_block_geojson": json.dumps({
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
            }
        }),
        "building_geojsons": [
            json.dumps({
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0.2, 0.2], [0.4, 0.2], [0.4, 0.4], [0.2, 0.4], [0.2, 0.2]]]
                }
            })
        ]
    }

    result_json = calculate_virtual_parcel(json.dumps(request))
    result = json.loads(result_json)

    assert "net_area_sqm" in result
    assert "virtual_parcel_geojson" in result
    assert result["net_area_sqm"] > 0
