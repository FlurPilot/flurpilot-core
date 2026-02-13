"use client";

import * as React from 'react';
import Map, { Source, Layer, MapRef } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { createClient } from '@/lib/supabase';

const parcelFillLayer = {
    id: 'parcels-fill',
    type: 'fill' as const,
    paint: {
        'fill-color': '#10b981',
        'fill-opacity': 0.2,
        'fill-outline-color': '#059669'
    }
};

const parcelLineLayer = {
    id: 'parcels-line',
    type: 'line' as const,
    paint: {
        'line-color': '#10b981',
        'line-width': 1
    }
};

// Virtual Parcels: Dashed line, slightly different visual to indicate "Calculated"
const virtualFillLayer = {
    id: 'virtual-fill',
    type: 'fill' as const,
    paint: {
        'fill-color': '#34d399',
        'fill-opacity': 0.3,
    }
};

const virtualLineLayer = {
    id: 'virtual-line',
    type: 'line' as const,
    paint: {
        'line-color': '#059669',
        'line-width': 2,
        'line-dasharray': [2, 2]
    }
};

interface GeoJSONFeature {
    geometry: {
        type: string;
        coordinates: number[] | number[][] | number[][][];
    };
}

interface ParcelsMapProps {
    onParcelSelect?: (feature: GeoJSONFeature) => void;
    focusedParcel?: GeoJSONFeature;
}

export default function ParcelsMap({ onParcelSelect, focusedParcel }: ParcelsMapProps) {
    // const { t } = useTranslations(); 
    const mapRef = React.useRef<MapRef>(null);

    // Data States
    const [realParcels, setRealParcels] = React.useState<GeoJSONFeature[] | null>(null);
    const [virtualParcels, setVirtualParcels] = React.useState<GeoJSONFeature[] | null>(null);

    // Watch focusedParcel for FlyTo
    React.useEffect(() => {
        if (focusedParcel && mapRef.current) {
            try {
                const geometry = focusedParcel.geometry;
                if (!geometry) return;

                // Get bounds manually or use a lib like @mapbox/geojson-extent (not installed)
                // Simple centroid logic for now
                let centerLng = 0;
                let centerLat = 0;

                // TODO: Implement proper centroid calculation
                // eslint-disable-next-line @typescript-eslint/no-unused-vars
                const getCenter = (_coords: number[][]) => {
                    return [0, 0];
                };

                // Quick FlyTo if Point
                if (geometry.type === 'Point') {
                    const coords = geometry.coordinates as number[];
                    centerLng = coords[0];
                    centerLat = coords[1];
                    mapRef.current.flyTo({ center: [centerLng, centerLat], zoom: 16 });
                }
            } catch (e) {
                console.error("FlyTo Error", e);
            }
        }
    }, [focusedParcel]);

    React.useEffect(() => {
        async function fetchRealParcels() {
            try {
                const supabase = createClient();
                const { data, error } = await supabase
                    .from('geo_parcels')
                    .select('id, alkis_id, geom, properties');

                if (error) throw error;

                if (data) {
                    interface ParcelData {
                        id: string;
                        alkis_id: string;
                        geom: GeoJSONFeature['geometry'];
                        properties: Record<string, unknown>;
                    }
                    const features = (data as ParcelData[]).map((item) => ({
                        type: 'Feature' as const,
                        geometry: item.geom,
                        properties: {
                            id: item.id,
                            type: 'real',
                            alkis_id: item.alkis_id,
                            ...item.properties
                        }
                    }));
                    setRealParcels(features);
                }
            } catch (err: unknown) {
                console.error("Real Parcels Error:", err);
            }
        }

        async function fetchVirtualParcels() {
            try {
                const supabase = createClient();
                const { data, error } = await supabase
                    .from('virtual_parcels')
                    .select('id, source_field_id, geometry, net_area_m2');

                if (error) throw error;

                if (data) {
                    interface VirtualParcelData {
                        id: string;
                        source_field_id: string;
                        geometry: GeoJSONFeature['geometry'];
                        net_area_m2: number;
                    }
                    const features = (data as VirtualParcelData[]).map((item) => ({
                        type: 'Feature' as const,
                        geometry: item.geometry,
                        properties: {
                            id: item.id,
                            type: 'virtual',
                            source: item.source_field_id,
                            area: item.net_area_m2
                        }
                    }));
                    setVirtualParcels(features);
                }
            } catch (err: unknown) {
                console.error("Virtual Parcels Error:", err);
            }
        }

        fetchRealParcels();
        fetchVirtualParcels();
    }, []);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const onClick = (event: any) => {
        const feature = event.features?.[0];
        if (feature && onParcelSelect) {
            onParcelSelect(feature);
        }
    };

    return (
        <div style={{ width: '100%', height: '100%', background: '#f8fafc' }}>
            <Map
                ref={mapRef}
                initialViewState={{
                    longitude: 11.5820, // Munich default
                    latitude: 48.1351,
                    zoom: 10
                }}
                style={{ width: '100%', height: '100%' }}
                mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
                interactiveLayerIds={['parcels-fill', 'virtual-fill']}
                onClick={onClick}
                cursor="pointer"
            >
                {/* 1. Real Parcels Layer */}
                {realParcels && (
                    <Source id="real-parcels" type="geojson" data={realParcels}>
                        <Layer {...parcelFillLayer} />
                        <Layer {...parcelLineLayer} />
                    </Source>
                )}

                {/* 2. Virtual Parcels Layer (On Top) */}
                {virtualParcels && (
                    <Source id="virtual-parcels" type="geojson" data={virtualParcels}>
                        <Layer {...virtualFillLayer} />
                        <Layer {...virtualLineLayer} />
                    </Source>
                )}
            </Map>
        </div>
    );
}
