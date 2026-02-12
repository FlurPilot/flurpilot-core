-- F-02: Virtual Parcel Engine (The Bavarian Bypass)
-- Stores calculated "Net Area" parcels (Field Block - Buildings)

create extension if not exists postgis;

-- 1. Create Table (Base structure if missing)
create table if not exists public.virtual_parcels (
    id uuid primary key default gen_random_uuid(),
    last_calculated_at timestamptz default now()
);

-- 2. Add Columns Robustly (Handling existing table)
alter table public.virtual_parcels 
add column if not exists source_field_id text;

alter table public.virtual_parcels 
add column if not exists net_area_m2 float;

alter table public.virtual_parcels 
add column if not exists geometry geometry(Polygon, 4326);

alter table public.virtual_parcels 
add column if not exists last_calculated_at timestamptz default now();

-- 3. Constraints & Indexes
do $$
begin
    -- Check if constraint exists
    if not exists (select 1 from pg_constraint where conname = 'uq_virtual_parcels_source') then
        
        -- PRE-ACTION: Remove Duplicates (Keep latest calculation)
        -- This fixes ERROR: 23505
        with duplicates as (
            select id,
            row_number() over (partition by source_field_id order by last_calculated_at desc) as rn
            from public.virtual_parcels
            where source_field_id is not null
        )
        delete from public.virtual_parcels
        where id in (select id from duplicates where rn > 1);
        
        -- Now add constraint
        alter table public.virtual_parcels add constraint uq_virtual_parcels_source unique (source_field_id);
    end if;
end $$;

-- Spatial Index for Fast Map Queries (Critical for Performance)
create index if not exists idx_virtual_parcels_geom 
on public.virtual_parcels using gist (geometry);

-- RLS: Enable security
alter table public.virtual_parcels enable row level security;

-- Policy: Public Read (for map)
drop policy if exists "Public Read Virtual Parcels" on public.virtual_parcels;
create policy "Public Read Virtual Parcels"
on public.virtual_parcels for select
using (true);

-- Policy: Service Role Write (for Worker)
drop policy if exists "Worker Write Virtual Parcels" on public.virtual_parcels;
create policy "Worker Write Virtual Parcels"
on public.virtual_parcels for all
using (true)
with check (true);


-- FUNCTION: Calculate Net Parcel
-- Inputs: Enclosing Field (GeoJSON), Array of Buildings (GeoJSON)
-- Output: The Difference Geometry (Polygon/MultiPolygon)
-- OPTIMIZATION: Use JSONB for RPC inputs to avoid PostgREST type matching issues.
-- OPTIMIZATION: Use ST_Area(geography) for global meter precision (no hardcoded UTM zones).
create or replace function calculate_net_parcel(
    field_geojson jsonb,
    building_geojsons jsonb[]
)
returns table (
    net_geom geometry(Polygon, 4326),
    net_area float
)
language plpgsql
as $$
declare
    field_geom geometry(Polygon, 4326);
    building_geoms geometry[];
    buildings_union geometry;
    diff_geom geometry;
    area_m2 float;
    b jsonb;
begin
    -- 1. Parse Inputs (Robust JSON handling)
    field_geom := ST_SetSRID(ST_GeomFromGeoJSON(field_geojson), 4326);
    
    -- Parse buildings array
    if array_length(building_geojsons, 1) is not null then
        foreach b in array building_geojsons
        loop
            building_geoms := array_append(building_geoms, ST_SetSRID(ST_GeomFromGeoJSON(b), 4326));
        end loop;
    end if;

    -- 2. Union all buildings
    if array_length(building_geoms, 1) is null then
        buildings_union := ST_GeomFromText('POLYGON EMPTY', 4326);
    else
        buildings_union := ST_Union(building_geoms);
    end if;

    -- 3. Perform Difference: Field - Buildings
    diff_geom := ST_Difference(field_geom, buildings_union);
    
    -- 4. Calculate Area (Global Precision)
    -- ST_Area(geography) calculates area on the spheroid (meters).
    -- This works for Bavaria, NRW, or Spain without changing SRID.
    area_m2 := ST_Area(diff_geom::geography);
    
    return query select diff_geom, area_m2;
end;
$$;
