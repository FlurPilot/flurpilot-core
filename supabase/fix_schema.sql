-- FIX: Add missing columns to existing waitlist table
-- Run this in Supabase SQL Editor if you get "Could not find the 'status' column" error

DO $$
BEGIN
    -- 1. Add 'status' column if missing
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'waitlist' AND column_name = 'status') THEN
        ALTER TABLE waitlist ADD COLUMN status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed'));
    END IF;

    -- 2. Add 'confirmation_token' column if missing
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'waitlist' AND column_name = 'confirmation_token') THEN
        ALTER TABLE waitlist ADD COLUMN confirmation_token UUID DEFAULT gen_random_uuid();
    END IF;

    -- 3. Add 'confirmed_at' column if missing
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'waitlist' AND column_name = 'confirmed_at') THEN
        ALTER TABLE waitlist ADD COLUMN confirmed_at TIMESTAMPTZ;
    END IF;

    -- 4. Add 'download_count' column if missing
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'waitlist' AND column_name = 'download_count') THEN
        ALTER TABLE waitlist ADD COLUMN download_count INTEGER DEFAULT 0;
    END IF;
END $$;

-- Force Schema Cache Reload (not easily commandable via SQL only in all envs, but DDL usually triggers it)
NOTIFY pgrst, 'reload schema';
