{{
    config(
        materialized='view'
    )
}}

with fhv as(
    select *
    from {{ source('staging','fhv') }}
    where dispatching_base_num is not null
)
select
    dispatching_base_num,
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,
    {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,
    SR_Flag,
    Affiliated_base_number
from fhv