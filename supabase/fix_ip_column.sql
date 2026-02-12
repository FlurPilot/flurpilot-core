-- FIX: Add missing signup_ip column
-- Run this in Supabase SQL Editor

ALTER TABLE waitlist ADD COLUMN IF NOT EXISTS signup_ip TEXT;

-- Reload Schema Cache
NOTIFY pgrst, 'reload schema';
