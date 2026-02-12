-- Enable pgcrypto for hashing
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create Audit Logs Table
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    actor_id UUID, -- Nullable for system actions or anonymous
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    details JSONB DEFAULT '{}'::jsonb,
    prev_hash TEXT,
    curr_hash TEXT
);

-- Index for fast retrieval of the last hash
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON public.audit_logs (timestamp DESC);

-- Function to Calculate Hash Chain
CREATE OR REPLACE FUNCTION public.calculate_audit_hash()
RETURNS TRIGGER AS $$
DECLARE
    last_hash TEXT;
    payload TEXT;
BEGIN
    -- 1. Get the hash of the most recent entry
    SELECT curr_hash INTO last_hash
    FROM public.audit_logs
    ORDER BY timestamp DESC, id DESC -- id tie-breaker
    LIMIT 1;

    -- If table is empty, seed with a genesis hash (e.g., all zeros)
    IF last_hash IS NULL THEN
        last_hash := '0000000000000000000000000000000000000000000000000000000000000000';
    END IF;

    -- 2. Store Previous Hash
    NEW.prev_hash := last_hash;

    -- 3. Calculate Current Hash
    -- Payload = Timestamp + Actor + Action + Resource + Details + PrevHash
    -- using HMAC logic or just SHA256. Simple SHA256 matches the requirement.
    payload := coalesce(NEW.timestamp::text, '') || 
               coalesce(NEW.actor_id::text, 'SYSTEM') || 
               coalesce(NEW.action, '') || 
               coalesce(NEW.resource, '') || 
               coalesce(NEW.details::text, '') || 
               last_hash;
               
    NEW.curr_hash := encode(digest(payload, 'sha256'), 'hex');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger
DROP TRIGGER IF EXISTS trigger_audit_log_insert ON public.audit_logs;
CREATE TRIGGER trigger_audit_log_insert
BEFORE INSERT ON public.audit_logs
FOR EACH ROW
EXECUTE FUNCTION public.calculate_audit_hash();

-- RLS: Read Only (Append Only effectively via Trigger, but let's lock it down)
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- No one can UPDATE or DELETE. Only INSERT.
CREATE POLICY "Enable insert for authenticated users and service_role"
ON public.audit_logs
FOR INSERT
TO authenticated, service_role
WITH CHECK (true);

-- Only Admins/Auditors can SELECT (view logs)
CREATE POLICY "Enable select for service_role only" -- Strict for now
ON public.audit_logs
FOR SELECT
TO service_role
USING (true);
