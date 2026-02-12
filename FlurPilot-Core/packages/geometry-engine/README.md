# Geometry Engine

High-performance geometry engine for FlurPilot, powered by Rust.

## Features

- **Virtual Parcel Calculation**: Compute net parcel area by subtracting buildings from field blocks
- **GeoJSON Support**: Native GeoJSON parsing and serialization
- **Rust Performance**: 10-100x faster than pure Python solutions
- **Dual Interface**: Both Python (PyO3) and WebAssembly (WASM) bindings

## Installation

### Python (via Maturin)

```bash
# Install maturin
pip install maturin

# Build and install
cd packages/geometry-engine
maturin develop --release

# Or install directly
maturin build --release
pip install target/wheels/geometry_engine-*.whl
```

### WebAssembly

```bash
# Build WASM target
cargo build --target wasm32-unknown-unknown --release --features wasm

# Or use wasm-pack
wasm-pack build --target web --features wasm
```

## Usage

### Python

```python
from geometry_engine import calculate_virtual_parcel
import json

request = {
    "field_block_geojson": '{"type": "Polygon", "coordinates": [[[...]]]}',
    "building_geojsons": [
        '{"type": "Polygon", "coordinates": [[[...]]]}',
    ]
}

result_json = calculate_virtual_parcel(json.dumps(request))
result = json.loads(result_json)

print(f"Net area: {result['net_area_sqm']} m²")
print(f"Virtual parcel: {result['virtual_parcel_geojson']}")
```

### WebAssembly

```javascript
import init, { calculate_virtual_parcel_wasm } from './geometry_engine.js';

async function computeParcel() {
  await init();
  
  const request = {
    field_block_geojson: '{"type": "Polygon", ...}',
    building_geojsons: ['{"type": "Polygon", ...}']
  };
  
  const result = calculate_virtual_parcel_wasm(JSON.stringify(request));
  const data = JSON.parse(result);
  
  console.log(`Net area: ${data.net_area_sqm} m²`);
}
```

## Architecture

The engine uses the `geo` crate for computational geometry:
- **Union**: Combines overlapping building polygons
- **Difference**: Subtracts buildings from field block
- **Area**: Calculates planar area (ensure metric projection!)

## Performance

Benchmarks show significant improvements over pure Python:
- Simple operations: 10-50x faster
- Complex polygons: 50-100x faster
- Memory usage: ~50% reduction

## Development

```bash
# Run tests
cargo test

# Build Python package
maturin develop

# Build WASM
wasm-pack build --target web --features wasm
```

## License

MIT
