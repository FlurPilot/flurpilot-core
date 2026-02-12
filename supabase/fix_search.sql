-- FIX: Enable Public Read for Search Data

-- 1. Scout Profiles (Cities)
ALTER TABLE scout_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Profiles" 
ON scout_profiles FOR SELECT 
TO anon, authenticated 
USING (true);

-- 2. Geo Parcels (Polygons)
ALTER TABLE geo_parcels ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Parcels" 
ON geo_parcels FOR SELECT 
TO anon, authenticated 
USING (true);

-- 3. Evidence Docs (Optional - for Intelligence Feed)
ALTER TABLE evidence_docs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Evidence" 
ON evidence_docs FOR SELECT 
TO anon, authenticated 
USING (true);
