-- Optimization: Global Deduplication Index
-- First, ensure the column exists (it was missing in early schemas)
alter table public.evidence_docs 
add column if not exists content_hash text;

-- Create the Index for O(1) Lookups
create index if not exists idx_evidence_docs_content_hash 
on public.evidence_docs (content_hash);
