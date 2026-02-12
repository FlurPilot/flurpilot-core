-- FlurPilot Supabase Schema
-- Run this in Supabase SQL Editor

-- 1. Waitlist Table for Lead Collection
CREATE TABLE IF NOT EXISTS waitlist (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    source TEXT DEFAULT 'landing_page',
    
    -- DOI Fields
    confirmation_token UUID DEFAULT gen_random_uuid(),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed')),
    confirmed_at TIMESTAMPTZ,
    signup_ip TEXT, -- IP address of the confirmation click (Proof of Consent)
    
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Index for faster email lookups
CREATE INDEX IF NOT EXISTS idx_waitlist_email ON waitlist(email);

-- 3. Row Level Security
ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;

-- 4. Policy: Only service role can access (for Edge Functions)
CREATE POLICY "Service role access only" ON waitlist
    FOR ALL
    USING (auth.role() = 'service_role');

-- 5. Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_waitlist_updated_at
    BEFORE UPDATE ON waitlist
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- 6. Analytics Table (optional, for tracking)
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    event_type TEXT NOT NULL, -- 'page_view', 'form_submit', 'download'
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on analytics
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role access only" ON analytics_events
    FOR ALL
    USING (auth.role() = 'service_role');
