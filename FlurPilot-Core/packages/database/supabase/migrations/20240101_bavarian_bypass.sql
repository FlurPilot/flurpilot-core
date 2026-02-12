-- Enable PostGIS if not already enabled
create extension if not exists postgis;

-- 1. Field Blocks (InVeKoS / Agricultural Land)
-- Source: Open Data or imported via Shapefile
create table if not exists field_blocks (
    id uuid primary key default gen_random_uuid(),
    code text, -- e.g. FLIK
    year int,
    geom geometry(Polygon, 4326)
);
create index if not exists field_blocks_geom_idx on field_blocks using gist(geom);

-- 2. Building Footprints (Hausumringe)
-- Source: ALKIS / Open Data
create table if not exists building_footprints (
    id uuid primary key default gen_random_uuid(),
    geom geometry(Polygon, 4326)
);
create index if not exists building_footprints_geom_idx on building_footprints using gist(geom);

-- 3. Virtual Parcels (The Result)
-- Derived Work: Field Block minus Buildings
create table if not exists virtual_parcels (
    id uuid primary key default gen_random_uuid(),
    source_field_id uuid references field_blocks(id),
    area_sqm float,
    geom geometry(MultiPolygon, 4326),
    created_at timestamptz default now()
);

-- 4. The Bavarian Bypass Logic
-- Subtracts all intersecting buildings from a field block
create or replace function calculate_virtual_parcel(field_block_id uuid)
returns uuid
language plpgsql
as $$
declare
    field_geom geometry;
    buildings_union geometry;
    result_geom geometry;
    new_id uuid;
begin
    -- Get Field Geometry
    select geom into field_geom from field_blocks where id = field_block_id;
    
    if field_geom is null then
        raise exception 'Field Block % not found', field_block_id;
    end if;

    -- Get Union of colliding buildings
    -- We only select buildings that actually intersect to keep it fast
    select ST_Union(geom) into buildings_union
    from building_footprints
    where ST_Intersects(geom, field_geom);

    if buildings_union is null then
        -- No buildings? The virtual parcel is the field block itself.
        result_geom := ST_Multi(field_geom);
    else
        -- Perform the Difference
        result_geom := ST_Multi(ST_Difference(field_geom, buildings_union));
    end if;

    -- Insert Result
    insert into virtual_parcels (source_field_id, area_sqm, geom)
    values (
        field_block_id,
        ST_Area(result_geom::geography), -- Calculate area in square meters
        result_geom
    )
    returning id into new_id;

    return new_id;
end;
$$;
