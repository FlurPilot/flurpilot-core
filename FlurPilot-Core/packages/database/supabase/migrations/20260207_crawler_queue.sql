-- Protocol F-01: Hybrid Acquisition Engine Queue
-- Table: crawler_jobs
-- Logic: Postgres-based Job Queue with Domain Locking and DLQ

create type job_status as enum ('pending', 'processing', 'completed', 'failed', 'dead');

create table if not exists public.crawler_jobs (
    id uuid not null default gen_random_uuid(),
    type text not null, -- 'crawl_profile', 'process_pdf'
    payload jsonb not null,
    status job_status not null default 'pending',
    
    -- Concurrency Control
    domain text, -- e.g. 'ris.moers.de'
    worker_id text, -- ID of the worker processing this (for crash recovery)
    
    -- Resilience
    retries int not null default 0,
    max_retries int not null default 3,
    error_log text,
    
    -- Timestamps
    created_at timestamptz not null default now(),
    started_at timestamptz,
    completed_at timestamptz,
    
    constraint crawler_jobs_pkey primary key (id)
);

-- Indexes for Speed
create index if not exists idx_crawler_jobs_status on public.crawler_jobs (status);
create index if not exists idx_crawler_jobs_domain on public.crawler_jobs (domain);

-- RLS (Worker Role needs access)
alter table public.crawler_jobs enable row level security;
create policy "Workers can access all jobs" on public.crawler_jobs for all using (true); -- Simplify for backend worker

-- FUNCTION: Atomic Fetch
-- "Give me the next job, BUT only if no other worker is processing this domain"
create or replace function public.fetch_next_job(p_worker_id text)
returns table (
    j_id uuid,
    j_type text,
    j_payload jsonb
) 
language plpgsql
as $$
declare
    v_job_id uuid;
begin
    -- 1. Identify a candidate job
    -- Criteria:
    --   a) Status is pending
    --   b) Its domain is NOT currently being processed by anyone else
    
    select id into v_job_id
    from public.crawler_jobs j
    where status = 'pending'
    and (
        domain is null 
        or 
        domain not in (
            select distinct domain 
            from public.crawler_jobs 
            where status = 'processing' 
            and domain is not null
            and started_at > now() - interval '1 hour' -- Safety: Ignore stuck jobs (handled by crash recovery later)
        )
    )
    order by created_at asc
    limit 1
    for update skip locked; -- Atomic Lock!
    
    -- 2. Claim the job
    if v_job_id is not null then
        update public.crawler_jobs
        set 
            status = 'processing',
            worker_id = p_worker_id,
            started_at = now()
        where id = v_job_id;
        
        return query select id, type, payload from public.crawler_jobs where id = v_job_id;
    end if;
    
    return;
end;
$$;
