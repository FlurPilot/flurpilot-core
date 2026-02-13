use geo::{Area, BooleanOps, MultiPolygon};
#[cfg(feature = "python")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::str::FromStr;
#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

// --- Version ---
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

// --- Data Structures ---

#[derive(Serialize, Deserialize)]
pub struct VirtualParcelRequest {
    pub field_block_geojson: String,
    pub building_geojsons: Vec<String>,
}

#[derive(Serialize, Deserialize)]
pub struct VirtualParcelResult {
    pub net_area_sqm: f64,
    pub virtual_parcel_geojson: String,
}

// --- Logic ---

fn parse_multipolygon(geojson_str: &str) -> Result<MultiPolygon<f64>, String> {
    let geo_json =
        geojson::GeoJson::from_str(geojson_str).map_err(|e| format!("Invalid GeoJSON: {}", e))?;

    let value = match geo_json {
        geojson::GeoJson::Geometry(g) => g.value,
        geojson::GeoJson::Feature(f) => f.geometry.ok_or("Feature has no geometry")?.value,
        geojson::GeoJson::FeatureCollection(_) => {
            return Err(
                "FeatureCollection not supported directly (must be Geometry or Feature)"
                    .to_string(),
            )
        }
    };

    let geo: geo_types::Geometry<f64> = value
        .try_into()
        .map_err(|e| format!("Failed to convert GeoJSON Value to Geometry: {}", e))?;

    match geo {
        geo_types::Geometry::Polygon(p) => Ok(MultiPolygon(vec![p])),
        geo_types::Geometry::MultiPolygon(mp) => Ok(mp),
        _ => Err("Input must be a Polygon or MultiPolygon".to_string()),
    }
}

fn internal_calculate_virtual_parcel(request_json: &str) -> Result<String, String> {
    let request: VirtualParcelRequest = serde_json::from_str(request_json)
        .map_err(|e| format!("Failed to parse request JSON: {}", e))?;

    // 1. Parse Field Block (Base)
    let field_block = parse_multipolygon(&request.field_block_geojson)?;

    // 2. Parse Buildings (Subtract) and Union them
    let mut buildings_union: MultiPolygon<f64> = MultiPolygon(vec![]);

    for building_geojson in request.building_geojsons {
        let building = parse_multipolygon(&building_geojson)?;
        buildings_union = buildings_union.union(&building);
    }

    // 3. Difference: Field - Buildings
    // Note: boolean_ops logic handles the geometric subtraction
    let virtual_parcel = field_block.difference(&buildings_union);

    // 4. Calculate Net Area (EPSG:25832 or similar metric projection assumed for now,
    // or we assume input is already projected. Geo-types Area is planar.)
    // TODO: Ensure input is projected (UTM) before calling this, otherwise area is invalid deg^2.
    let net_area = virtual_parcel.unsigned_area();

    // 5. Serialize Result
    let result_geojson = geojson::Geometry::from(&virtual_parcel).to_string();

    let result = VirtualParcelResult {
        net_area_sqm: net_area, // Warning: Checks regarding projection needed in caller!
        virtual_parcel_geojson: result_geojson,
    };

    serde_json::to_string(&result).map_err(|e| format!("Failed to serialize result: {}", e))
}

// --- Python Interface ---

#[cfg(feature = "python")]
#[pyfunction]
fn calculate_virtual_parcel(request_json: String) -> PyResult<String> {
    internal_calculate_virtual_parcel(&request_json)
        .map_err(PyErr::new::<pyo3::exceptions::PyValueError, _>)
}

#[cfg(feature = "python")]
#[pyfunction]
fn get_version() -> &'static str {
    VERSION
}

#[cfg(feature = "python")]
#[pymodule]
fn geometry_engine(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_virtual_parcel, m)?)?;
    m.add_function(wrap_pyfunction!(get_version, m)?)?;
    m.add("__version__", VERSION)?;
    Ok(())
}

// --- WASM Interface ---

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn calculate_virtual_parcel_wasm(request_json: String) -> Result<String, String> {
    #[cfg(feature = "wasm")]
    console_error_panic_hook::set_once();
    internal_calculate_virtual_parcel(&request_json)
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn get_version_wasm() -> String {
    VERSION.to_string()
}
