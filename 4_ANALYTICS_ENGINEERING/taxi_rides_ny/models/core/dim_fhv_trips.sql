{{
    config(
        materialized='table'
    )
}}

with fhv as (
    select *, 
    from {{ ref('stg_fhv') }}
), 
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select
    pickup_zone.zone as pu_zone,
    dropoff_zone.zone as do_zone,
    dropoff_datetime,
    pickup_datetime,
    pickup_locationid,
    dropoff_locationid,
    extract(year from pickup_datetime) as year,
    extract(month from pickup_datetime) as month
from fhv
inner join dim_zones as pickup_zone
on fhv.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv.dropoff_locationid = dropoff_zone.locationid