{{
    config(
        materialized='table'
    )
}}

with percentiles as
(
    select
        year,
        month,
        pu_zone,
        do_zone,
        percentile_cont(date_diff(dropoff_datetime, pickup_datetime, minute), 0.9) over (partition by year, month, pickup_locationid, dropoff_locationid) as p90
    from {{ ref('dim_fhv_trips') }}
)
select * from percentiles
group by
    year,
    month,
    pu_zone,
    do_zone,
    p90