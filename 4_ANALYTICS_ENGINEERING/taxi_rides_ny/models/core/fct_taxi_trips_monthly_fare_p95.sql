{{
    config(
        materialized='table'
    )
}}

with percentiles as
(
    select
        service_type,
        year,
        month,
        percentile_cont(fare_amount, 0.97) over (partition by service_type, year, month) as p97,
        percentile_cont(fare_amount, 0.95) over (partition by service_type, year, month) as p95,
        percentile_cont(fare_amount, 0.9) over (partition by service_type, year, month) as p90
    from {{ ref('fact_trips') }}
        where fare_amount > 0
        and trip_distance > 0
        and payment_type_description in ('Cash', 'Credit card')
)
select * from percentiles
group by
  service_type,
  year,
  month,
  p97,
  p95,
  p90