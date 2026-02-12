"use client";

import { useEffect, useState } from 'react';
import type { initSync } from 'geometry-engine'; // Type-only import if available, or any

type GeometryEngineModule = {
    calculate_virtual_parcel_wasm: (json: string) => string;
    default: unknown;
    initSync: typeof initSync;
};

export function useGeometryEngine() {
    const [engine, setEngine] = useState<GeometryEngineModule | null>(null);
    const [isReady, setIsReady] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        async function loadWasm() {
            try {
                // Dynamic import for WASM module
                // @ts-expect-error - The module is generated at build time
                const mod = await import('geometry-engine');
                await mod.default(); // Initialize WASM
                setEngine(mod);
                setIsReady(true);
            } catch (err) {
                console.error("Failed to load WASM engine:", err);
                setError(err instanceof Error ? err : new Error('Unknown WASM load error'));
            }
        }

        loadWasm();
    }, []);

    const calculateVirtualParcel = (fieldBlockGeoJson: string, buildingGeoJsons: string[]) => {
        if (!engine || !isReady) {
            throw new Error("Geometry Engine not ready");
        }

        const request = JSON.stringify({
            field_block_geojson: fieldBlockGeoJson,
            building_geojsons: buildingGeoJsons,
        });

        try {
            const resultJson = engine.calculate_virtual_parcel_wasm(request);
            return JSON.parse(resultJson);
        } catch (e) {
            console.error("WASM Calculation Error:", e);
            throw e;
        }
    };

    return { isReady, error, calculateVirtualParcel };
}
