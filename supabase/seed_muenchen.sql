-- Insert München for Tier 2 Testing
INSERT INTO scout_profiles (name, oparl_url, active)
VALUES ('Stadt München', NULL, TRUE)
ON CONFLICT (name) DO NOTHING;
