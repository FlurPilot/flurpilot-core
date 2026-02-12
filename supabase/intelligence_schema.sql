-- FlurPilot Intelligence Schema
-- Stores municipal data harvested by the Worker

-- 1. Scout Profiles (Municipalities being monitored)
CREATE TABLE IF NOT EXISTS scout_profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    oparl_url TEXT,
    active BOOLEAN DEFAULT TRUE,
    lat FLOAT8, -- Geocenter latitude
    lon FLOAT8, -- Geocenter longitude
    last_scout_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Evidence Docs (Papers/Beschlüsse found via OParl)
CREATE TABLE IF NOT EXISTS evidence_docs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    external_id TEXT UNIQUE, -- OParl ID
    title TEXT,
    doc_type TEXT, -- 'Drucksache', 'Beschluss'
    published_date DATE,
    url TEXT, -- Link to RIS
    region_id UUID REFERENCES scout_profiles(id),
    
    -- AI Analysis
    relevant BOOLEAN DEFAULT FALSE,
    risk_score INTEGER DEFAULT 0, -- 0-100
    summary TEXT,
    extracted_locations JSONB DEFAULT '[]', -- Geoparsed addresses/parcels
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Geo Parcels (The "Map")
-- Note: Requires PostGIS extension, but we use standard floats/json for MVP if PostGIS not available
-- Ideally: location GEOGRAPHY(Polygon, 4326)
CREATE TABLE IF NOT EXISTS geo_parcels (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    alkis_id TEXT UNIQUE,
    
    -- Geometry (stored as GeoJSON or WKT if PostGIS is tricky on free tier)
    geometry JSONB, 
    center_lat FLOAT8,
    center_lon FLOAT8,
    
    -- Properties
    owner_name TEXT, -- Mocked/Private
    area_sqm FLOAT8,
    usage_type TEXT, -- 'Ackerland', 'Forst', 'Siedlung'
    
    -- Intelligence Link
    risk_score INTEGER DEFAULT 0, -- Aggregated from Evidence
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_evidence_region ON evidence_docs(region_id);
CREATE INDEX IF NOT EXISTS idx_parcels_alkis ON geo_parcels(alkis_id);

-- Enable RLS
ALTER TABLE scout_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_docs ENABLE ROW LEVEL SECURITY;
ALTER TABLE geo_parcels ENABLE ROW LEVEL SECURITY;

-- Service Role Policy (The Worker needs full access)
DROP POLICY IF EXISTS "Worker full access scout_profiles" ON scout_profiles;
CREATE POLICY "Worker full access scout_profiles" ON scout_profiles FOR ALL USING (auth.role() = 'service_role');

DROP POLICY IF EXISTS "Worker full access evidence_docs" ON evidence_docs;
CREATE POLICY "Worker full access evidence_docs" ON evidence_docs FOR ALL USING (auth.role() = 'service_role');

DROP POLICY IF EXISTS "Worker full access geo_parcels" ON geo_parcels;
CREATE POLICY "Worker full access geo_parcels" ON geo_parcels FOR ALL USING (auth.role() = 'service_role');

-- Public Read Policy (for Dashboard)
-- TODO: Restrict to authenticated users later
DROP POLICY IF EXISTS "Public read scout_profiles" ON scout_profiles;
CREATE POLICY "Public read scout_profiles" ON scout_profiles FOR SELECT USING (true);

DROP POLICY IF EXISTS "Public read evidence_docs" ON evidence_docs;
CREATE POLICY "Public read evidence_docs" ON evidence_docs FOR SELECT USING (true);

DROP POLICY IF EXISTS "Public read geo_parcels" ON geo_parcels;
CREATE POLICY "Public read geo_parcels" ON geo_parcels FOR SELECT USING (true);
