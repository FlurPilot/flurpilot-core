import pytest
import json
from geometry_engine import calculate_virtual_parcel, __version__


def test_version():
    """Test that version is available"""
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__.split('.')) >= 2


def test_simple_parcel_calculation():
    """Test basic virtual parcel calculation"""
    # Create a simple square field block (100x100m)
    field_block = {
        "type": "Polygon",
        "coordinates": [[
            [0, 0],
            [100, 0],
            [100, 100],
            [0, 100],
            [0, 0]
        ]]
    }
    
    # Create a building (10x10m) in the corner
    building = {
        "type": "Polygon",
        "coordinates": [[
            [0, 0],
            [10, 0],
            [10, 10],
            [0, 10],
            [0, 0]
        ]]
    }
    
    request = {
        "field_block_geojson": json.dumps(field_block),
        "building_geojsons": [json.dumps(building)]
    }
    
    result_json = calculate_virtual_parcel(json.dumps(request))
    result = json.loads(result_json)
    
    # Should be 9900 m² (10000 - 100)
    assert result['net_area_sqm'] == pytest.approx(9900.0, abs=1.0)
    assert 'virtual_parcel_geojson' in result


def test_no_buildings():
    """Test calculation with no buildings"""
    field_block = {
        "type": "Polygon",
        "coordinates": [[
            [0, 0],
            [50, 0],
            [50, 50],
            [0, 50],
            [0, 0]
        ]]
    }
    
    request = {
        "field_block_geojson": json.dumps(field_block),
        "building_geojsons": []
    }
    
    result_json = calculate_virtual_parcel(json.dumps(request))
    result = json.loads(result_json)
    
    # Should be full area (2500 m²)
    assert result['net_area_sqm'] == pytest.approx(2500.0, abs=1.0)


def test_multiple_buildings():
    """Test with multiple overlapping buildings"""
    field_block = {
        "type": "Polygon",
        "coordinates": [[
            [0, 0],
            [100, 0],
            [100, 100],
            [0, 100],
            [0, 0]
        ]]
    }
    
    # Two overlapping buildings
    building1 = {
        "type": "Polygon",
        "coordinates": [[
            [0, 0], [30, 0], [30, 30], [0, 30], [0, 0]
        ]]
    }
    building2 = {
        "type": "Polygon",
        "coordinates": [[
            [20, 20], [50, 20], [50, 50], [20, 50], [20, 20]
        ]]
    }
    
    request = {
        "field_block_geojson": json.dumps(field_block),
        "building_geojsons": [
            json.dumps(building1),
            json.dumps(building2)
        ]
    }
    
    result_json = calculate_virtual_parcel(json.dumps(request))
    result = json.loads(result_json)
    
    # Union of buildings should be ~1900 m², so net should be ~8100 m²
    assert result['net_area_sqm'] < 9000.0
    assert result['net_area_sqm'] > 8000.0


def test_geojson_feature():
    """Test with GeoJSON Feature format"""
    feature = {
        "type": "Feature",
        "properties": {"id": "test"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [0, 0], [10, 0], [10, 10], [0, 10], [0, 0]
            ]]
        }
    }
    
    request = {
        "field_block_geojson": json.dumps(feature),
        "building_geojsons": []
    }
    
    result_json = calculate_virtual_parcel(json.dumps(request))
    result = json.loads(result_json)
    
    assert result['net_area_sqm'] == pytest.approx(100.0, abs=1.0)


# Benchmark tests (optional, requires pytest-benchmark)
class TestBenchmarks:
    def test_benchmark_simple(self, benchmark):
        """Benchmark simple calculation"""
        field_block = {
            "type": "Polygon",
            "coordinates": [[
                [0, 0], [1000, 0], [1000, 1000], [0, 1000], [0, 0]
            ]]
        }
        
        request = {
            "field_block_geojson": json.dumps(field_block),
            "building_geojsons": []
        }
        
        request_json = json.dumps(request)
        result = benchmark(calculate_virtual_parcel, request_json)
        
        # Verify result is valid
        data = json.loads(result)
        assert data['net_area_sqm'] > 0
