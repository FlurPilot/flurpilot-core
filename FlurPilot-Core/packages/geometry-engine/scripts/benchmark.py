#!/usr/bin/env python3
"""
Benchmark: Python/Shapely vs Rust/Geometry Engine

This script compares the performance of the Rust geometry engine
against the pure Python/Shapely implementation used in Supabase RPC.

Target: 10x speedup for complex operations
"""

import json
import time
import statistics
from geometry_engine import calculate_virtual_parcel
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
import sys


def create_test_polygons(complexity="simple"):
    """Create test polygons of varying complexity."""
    if complexity == "simple":
        # Simple square field block
        field = {
            "type": "Polygon",
            "coordinates": [[
                [0, 0], [1000, 0], [1000, 1000], [0, 1000], [0, 0]
            ]]
        }
        # Single building
        buildings = [{
            "type": "Polygon",
            "coordinates": [[
                [100, 100], [200, 100], [200, 200], [100, 200], [100, 100]
            ]]
        }]
    
    elif complexity == "medium":
        # Larger field with 10 buildings
        field = {
            "type": "Polygon",
            "coordinates": [[
                [0, 0], [5000, 0], [5000, 5000], [0, 5000], [0, 0]
            ]]
        }
        buildings = []
        for i in range(10):
            x = (i % 5) * 800 + 100
            y = (i // 5) * 800 + 100
            buildings.append({
                "type": "Polygon",
                "coordinates": [[
                    [x, y], [x+200, y], [x+200, y+200], [x, y+200], [x, y]
                ]]
            })
    
    elif complexity == "complex":
        # Complex field with 50 overlapping buildings
        field = {
            "type": "Polygon",
            "coordinates": [[
                [0, 0], [10000, 0], [10000, 10000], [0, 10000], [0, 0]
            ]]
        }
        buildings = []
        for i in range(50):
            x = (i % 10) * 900 + 50
            y = (i // 10) * 900 + 50
            # Some overlapping buildings
            overlap = 50 if i % 3 == 0 else 0
            buildings.append({
                "type": "Polygon",
                "coordinates": [[
                    [x, y], [x+300-overlap, y], [x+300-overlap, y+300-overlap], 
                    [x, y+300-overlap], [x, y]
                ]]
            })
    
    else:
        raise ValueError(f"Unknown complexity: {complexity}")
    
    return field, buildings


def benchmark_rust(field, buildings, iterations=100):
    """Benchmark Rust implementation."""
    request = {
        "field_block_geojson": json.dumps(field),
        "building_geojsons": [json.dumps(b) for b in buildings]
    }
    request_json = json.dumps(request)
    
    # Warmup
    for _ in range(5):
        result = calculate_virtual_parcel(request_json)
        assert json.loads(result)['net_area_sqm'] > 0
    
    # Benchmark
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        result = calculate_virtual_parcel(request_json)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    return {
        "mean_ms": statistics.mean(times),
        "median_ms": statistics.median(times),
        "min_ms": min(times),
        "max_ms": max(times),
        "stdev_ms": statistics.stdev(times) if len(times) > 1 else 0
    }


def benchmark_python(field, buildings, iterations=100):
    """Benchmark Python/Shapely implementation."""
    field_shape = shape(field)
    building_shapes = [shape(b) for b in buildings]
    
    # Warmup
    for _ in range(5):
        if building_shapes:
            buildings_union = unary_union(building_shapes)
            result = field_shape.difference(buildings_union)
            area = result.area
        else:
            area = field_shape.area
        assert area > 0
    
    # Benchmark
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        if building_shapes:
            buildings_union = unary_union(building_shapes)
            result = field_shape.difference(buildings_union)
            area = result.area
        else:
            area = field_shape.area
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    return {
        "mean_ms": statistics.mean(times),
        "median_ms": statistics.median(times),
        "min_ms": min(times),
        "max_ms": max(times),
        "stdev_ms": statistics.stdev(times) if len(times) > 1 else 0
    }


def run_benchmark(complexity, iterations):
    """Run benchmark for a specific complexity level."""
    print(f"\n{'='*60}")
    print(f"Benchmark: {complexity.upper()} Complexity")
    print(f"Iterations: {iterations}")
    print(f"{'='*60}")
    
    field, buildings = create_test_polygons(complexity)
    print(f"Field vertices: {len(field['coordinates'][0])}")
    print(f"Building count: {len(buildings)}")
    
    print("\n🔧 Rust Geometry Engine...")
    rust_results = benchmark_rust(field, buildings, iterations)
    
    print("🐍 Python/Shapely...")
    python_results = benchmark_python(field, buildings, iterations)
    
    speedup = python_results['mean_ms'] / rust_results['mean_ms']
    
    print(f"\n📊 Results:")
    print(f"  Rust:   {rust_results['mean_ms']:.3f} ms (±{rust_results['stdev_ms']:.3f})")
    print(f"  Python: {python_results['mean_ms']:.3f} ms (±{python_results['stdev_ms']:.3f})")
    print(f"  Speedup: {speedup:.1f}x {'✅' if speedup >= 10 else '⚠️'}")
    
    return {
        "complexity": complexity,
        "rust": rust_results,
        "python": python_results,
        "speedup": speedup
    }


def main():
    print("="*60)
    print("Geometry Engine Performance Benchmark")
    print("Comparing Rust vs Python/Shapely implementations")
    print("="*60)
    
    results = []
    
    # Run benchmarks with different complexities
    results.append(run_benchmark("simple", iterations=1000))
    results.append(run_benchmark("medium", iterations=500))
    results.append(run_benchmark("complex", iterations=100))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for r in results:
        status = "✅" if r['speedup'] >= 10 else "⚠️" if r['speedup'] >= 5 else "❌"
        print(f"{r['complexity']:10} | {r['speedup']:6.1f}x {status}")
    
    avg_speedup = statistics.mean([r['speedup'] for r in results])
    print(f"\nAverage speedup: {avg_speedup:.1f}x")
    
    if avg_speedup >= 10:
        print("🎉 Target achieved: 10x speedup!")
        return 0
    elif avg_speedup >= 5:
        print("⚠️  Good but below 10x target")
        return 0
    else:
        print("❌ Below performance target")
        return 1


if __name__ == "__main__":
    sys.exit(main())
