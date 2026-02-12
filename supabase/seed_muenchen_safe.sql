-- SAFE INSERT for München (Workaround for missing Unique Constraint)
INSERT INTO scout_profiles (name, oparl_url, active)
SELECT 'Stadt München', NULL, TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM scout_profiles WHERE name = 'Stadt München'
);
