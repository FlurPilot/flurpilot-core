-- 1. Enable PostGIS (GIS Capabilities)
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Create Parcels Table (Virtual Parcel Engine)
CREATE TABLE IF NOT EXISTS public.geo_parcels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alkis_id TEXT UNIQUE,       -- Eindeutige Flurstücksnummer
    geom GEOMETRY(POLYGON, 4326), -- Die Koordinaten (GPS)
    area_sqm NUMERIC,           -- Fläche in qm
    properties JSONB,           -- Zusatzdaten (Nutzung, Eigentümer-Typ)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Create Spatial Index (Speed up map searches)
CREATE INDEX idx_geo_parcels_geom ON public.geo_parcels USING GIST (geom);

-- 4. Enable RLS
ALTER TABLE public.geo_parcels ENABLE ROW LEVEL SECURITY;

-- 5. Policies
CREATE POLICY "Allow public read" ON public.geo_parcels
    FOR SELECT TO anon, authenticated USING (true);

CREATE POLICY "Allow service write" ON public.geo_parcels
    FOR ALL TO service_role USING (true);
