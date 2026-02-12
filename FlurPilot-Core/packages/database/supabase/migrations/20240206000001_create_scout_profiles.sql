-- Create the Scout Profiles table to manage municipality targets
CREATE TABLE IF NOT EXISTS public.scout_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    ags TEXT UNIQUE, -- Amtlicher Gemeindeschluessel
    oparl_url TEXT,
    active BOOLEAN DEFAULT true,
    last_scout_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.scout_profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Allow read access to authenticated users (including service role)
CREATE POLICY "Allow read for authenticated" ON public.scout_profiles
    FOR SELECT TO authenticated USING (true);

-- Policy: Allow service role full access
CREATE POLICY "Allow full access for service role" ON public.scout_profiles
    FOR ALL TO service_role USING (true);

-- Insert 'Niederkruechten' (Example) if not exists
INSERT INTO public.scout_profiles (name, ags, oparl_url)
VALUES (
    'Niederkrüchten', 
    '05166016', 
    'https://sdnetrim.kdvz-frechen.de/rim4390/api/oparl/1.0/system'
) ON CONFLICT (ags) DO NOTHING;
