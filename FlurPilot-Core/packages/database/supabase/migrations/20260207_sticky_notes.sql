-- Migration: Create sticky_notes table for Client-Side Encrypted Data
-- Description: Stores encrypted blobs. Server has NO access to plaintext.

create table if not exists public.sticky_notes (
    id uuid not null default gen_random_uuid(),
    parcel_id text not null, -- Links to the parcel (e.g., Flurstückskennzeichen)
    user_id uuid not null default auth.uid(), -- Owner of the note
    
    -- Encrypted Data Blob (JSONB)
    -- Contains: ciphertext, iv, salt, wrappedKeyUser
    encrypted_blob jsonb not null,
    
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    
    constraint sticky_notes_pkey primary key (id),
    constraint sticky_notes_user_id_fkey foreign key (user_id) references auth.users(id) on delete cascade
);

-- Indexes
create index if not exists sticky_notes_parcel_id_idx on public.sticky_notes (parcel_id);
create index if not exists sticky_notes_user_id_idx on public.sticky_notes (user_id);

-- RLS (Row Level Security)
alter table public.sticky_notes enable row level security;

-- Policy: Users can only see their own notes
create policy "Users can view their own notes"
    on public.sticky_notes
    for select
    using (auth.uid() = user_id);

create policy "Users can insert their own notes"
    on public.sticky_notes
    for insert
    with check (auth.uid() = user_id);

create policy "Users can update their own notes"
    on public.sticky_notes
    for update
    using (auth.uid() = user_id);

create policy "Users can delete their own notes"
    on public.sticky_notes
    for delete
    using (auth.uid() = user_id);

-- Audit Trail Trigger (Zero Knowledge Access Log)
-- We log WHEN a record was accessed, but we can't see WHAT was inside.
-- Note: 'select' triggers are expensive/complex in PG. 
-- We usually log access via the Application API or using pgAudit. 
-- For now, we rely on the standard Supabase logs and Last Access timestamp updating if feasible.
