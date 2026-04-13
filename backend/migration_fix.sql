-- =====================================================
-- PostgreSQL Migration Script for LIFEASY V27
-- Fixes: Missing is_verified and is_active columns
-- Run this on Render PostgreSQL database
-- =====================================================

-- Step 1: Add is_verified column if it doesn't exist
ALTER TABLE tenants 
ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;

-- Step 2: Add is_active column if it doesn't exist
ALTER TABLE tenants 
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT FALSE;

-- Step 3: Add profile_photo column if it doesn't exist
ALTER TABLE tenants 
ADD COLUMN IF NOT EXISTS profile_photo TEXT;

-- Step 4: Update existing tenants to be verified and active
-- (This ensures existing users can login immediately)
UPDATE tenants 
SET is_verified = TRUE 
WHERE is_verified IS NULL OR is_verified = FALSE;

UPDATE tenants 
SET is_active = TRUE 
WHERE is_active IS NULL OR is_active = FALSE;

-- Step 5: Verify the changes
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'tenants'
AND column_name IN ('is_verified', 'is_active', 'profile_photo')
ORDER BY column_name;

-- =====================================================
-- VERIFICATION QUERY
-- Run this separately to check your specific email
-- =====================================================
-- SELECT * FROM tenants WHERE email='majadar1din@gmail.com';

-- =====================================================
-- NOTES:
-- =====================================================
-- 1. Run this script in Render PostgreSQL console
-- 2. All existing tenants will be marked as verified & active
-- 3. New registrations will follow proper approval workflow
-- 4. IF NOT EXISTS ensures safe re-runs
