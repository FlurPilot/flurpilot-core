import { createClient } from '@supabase/supabase-js';

// Shared Supabase Clients (Admin & Anon)
export const supabase = (url: string, key: string) => createClient(url, key);
