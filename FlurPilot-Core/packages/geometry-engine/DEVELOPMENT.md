# Development Guide - Geometry Engine

This guide helps you set up and develop the Rust Geometry Engine locally.

## Prerequisites

- **Rust** (latest stable): Install from [rustup.rs](https://rustup.rs/)
- **Python** 3.11+: Required for building Python bindings
- **Maturin**: Python build tool for Rust

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Maturin
pip install maturin
```

## Quick Start

```bash
cd packages/geometry-engine

# Build and install in development mode
make develop

# Run tests
make test

# Run benchmarks
make benchmark
```

## Project Structure

```
packages/geometry-engine/
├── Cargo.toml              # Rust package configuration
├── pyproject.toml          # Python package configuration
├── Makefile               # Common build commands
├── src/
│   └── lib.rs             # Core Rust implementation
├── python/
│   └── geometry_engine/   # Python package wrapper
│       └── __init__.py
├── tests/
│   └── test_geometry_engine.py  # Python tests
└── scripts/
    └── benchmark.py       # Performance benchmarks
```

## Development Workflow

### 1. Making Changes to Rust Code

Edit `src/lib.rs` and then:

```bash
# Check code without building
cargo check

# Format code
cargo fmt

# Run linter
cargo clippy

# Run Rust tests
cargo test
```

### 2. Testing Python Bindings

After making changes:

```bash
# Rebuild and install
make develop

# Run Python tests
pytest tests/ -v
```

### 3. Running Benchmarks

```bash
# Make sure shapely is installed
pip install shapely

# Run benchmarks
python scripts/benchmark.py
```

## Architecture

### Core Functions

The engine uses the `geo` crate for computational geometry:

1. **union()**: Combines overlapping building polygons
   - Used to merge multiple buildings before subtraction
   - Handles overlapping geometries correctly

2. **difference()**: Subtracts buildings from field block
   - Core operation for virtual parcel calculation
   - Returns the remaining area after subtraction

3. **unsigned_area()**: Calculates planar area
   - Returns area in square units of the coordinate system
   - **Important**: Input must be in a metric projection (e.g., EPSG:25832)
   - Using degrees (EPSG:4326) will give incorrect results

### Data Flow

```
Python Request (JSON)
    ↓
Rust: Parse GeoJSON → geo-types
    ↓
Rust: Union buildings
    ↓
Rust: Difference (Field - Buildings)
    ↓
Rust: Calculate area
    ↓
Rust: Serialize result → JSON
    ↓
Python Response
```

## API Reference

### Python Interface

```python
from geometry_engine import calculate_virtual_parcel

request = {
    "field_block_geojson": json.dumps({
        "type": "Polygon",
        "coordinates": [[[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]]]
    }),
    "building_geojsons": [
        json.dumps({
            "type": "Polygon",
            "coordinates": [[[10, 10], [20, 10], [20, 20], [10, 20], [10, 10]]]
        })
    ]
}

result_json = calculate_virtual_parcel(json.dumps(request))
result = json.loads(result_json)
# result = {
#     "net_area_sqm": 9900.0,
#     "virtual_parcel_geojson": "{...}"
# }
```

### Error Handling

The function returns a JSON string on success. On error, it raises a Python `ValueError`.

### WASM Interface

```javascript
import init, { calculate_virtual_parcel_wasm } from './geometry_engine.js';

async function compute() {
    await init();
    const request = {
        field_block_geojson: '{"type": "Polygon", ...}',
        building_geojsons: ['{"type": "Polygon", ...}']
    };
    const result = calculate_virtual_parcel_wasm(JSON.stringify(request));
    return JSON.parse(result);
}
```

## Common Issues

### Build Failures

**Issue**: `error: linker cc not found`
**Solution**: Install build essentials:
- Ubuntu/Debian: `sudo apt-get install build-essential`
- macOS: Install Xcode command line tools
- Windows: Install Visual Studio Build Tools

**Issue**: Python import fails with "undefined symbol"
**Solution**: Rebuild with `make develop` and ensure you're using the same Python version

### Performance Issues

**Issue**: Benchmarks show no speedup
**Solution**: 
- Ensure you're running release builds: `maturin develop --release`
- Check that input coordinates are in metric projection (not degrees)

### Test Failures

**Issue**: Tests fail with geometry errors
**Solution**: Check that GeoJSON is valid and polygons are closed (first and last point identical)

## Debugging

### Rust Debugging

```bash
# Run with backtrace
cargo test -- --nocapture
RUST_BACKTRACE=1 cargo test
```

### Python Debugging

```python
import geometry_engine

# Enable detailed error messages
try:
    result = geometry_engine.calculate_virtual_parcel(request)
except ValueError as e:
    print(f"Error: {e}")
```

## Building for Production

### Python Wheels

```bash
# Build wheels for distribution
maturin build --release

# Wheels will be in target/wheels/
```

### WebAssembly

```bash
# Build WASM target
cargo build --target wasm32-unknown-unknown --release --no-default-features --features wasm

# Or use wasm-pack
wasm-pack build --target web --no-default-features --features wasm
```

## Contributing

1. Write tests for new features
2. Run `make check` before committing
3. Ensure benchmarks don't regress
4. Update documentation for API changes

## Resources

- [geo crate documentation](https://docs.rs/geo/latest/geo/)
- [PyO3 documentation](https://pyo3.rs/)
- [Maturin documentation](https://www.maturin.rs/)
- [GeoJSON specification](https://geojson.org/)

## Support

For issues or questions:
1. Check this guide first
2. Look at existing tests for examples
3. Review the benchmark script for usage patterns
