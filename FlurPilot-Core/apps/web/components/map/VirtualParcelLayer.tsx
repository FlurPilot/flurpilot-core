"use client";

import { useLayoutEffect, useState, useCallback } from 'react';
import { Feature, Geometry, GeoJsonProperties } from 'geojson';
import { useGeometryEngine } from '@/hooks/useGeometryEngine';
import { Source, Layer } from 'react-map-gl/maplibre';

type GeoJSONFeature = Feature<Geometry, GeoJsonProperties>;

interface VirtualParcelLayerProps {
    fieldBlock: GeoJSONFeature;
    buildings: GeoJSONFeature[];
}

interface VirtualParcelResult {
    virtual_parcel_geojson: string;
}

export function VirtualParcelLayer({ fieldBlock, buildings }: VirtualParcelLayerProps) {
    const { isReady, calculateVirtualParcel, error } = useGeometryEngine();
    const [virtualParcel, setVirtualParcel] = useState<GeoJSONFeature | null>(null);

    const calculateParcel = useCallback(() => {
        if (isReady && fieldBlock && buildings) {
            try {
                const fieldJson = JSON.stringify(fieldBlock.geometry);
                const buildingJsons = buildings.map(b => JSON.stringify(b.geometry));

                const result = calculateVirtualParcel(fieldJson, buildingJsons) as VirtualParcelResult;
                setVirtualParcel(JSON.parse(result.virtual_parcel_geojson) as GeoJSONFeature);
            } catch (e) {
                console.error("Failed to calculate virtual parcel:", e);
            }
        }
    }, [isReady, fieldBlock, buildings, calculateVirtualParcel]);

    useLayoutEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        calculateParcel();
    }, [calculateParcel]);

    if (error) return null;
    if (!virtualParcel) return null;

    return (
        <Source id="virtual-parcel" type="geojson" data={virtualParcel}>
            <Layer
                id="virtual-parcel-fill"
                type="fill"
                paint={{
                    'fill-color': '#10b981', // Emerald-500
                    'fill-opacity': 0.4,
                    'fill-outline-color': '#059669', // Emerald-600
                }}
            />
            <Layer
                id="virtual-parcel-line"
                type="line"
                paint={{
                    'line-color': '#059669',
                    'line-width': 2,
                }}
            />
        </Source>
    );
}
