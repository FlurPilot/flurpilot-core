-- DATA REPAIR SCRIPT
-- Run this to fix the missing columns in your database

-- 1. Add missing Geolocation columns
ALTER TABLE scout_profiles ADD COLUMN IF NOT EXISTS lat FLOAT8;
ALTER TABLE scout_profiles ADD COLUMN IF NOT EXISTS lon FLOAT8;

-- 2. Cleanup old/broken entries
DELETE FROM scout_profiles WHERE name = 'Niederkrüchten';

-- 3. Verify
SELECT * FROM scout_profiles;
