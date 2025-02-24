{{
    config(
        materialized='table'
    )
}}

select
    t1.service_type,
    t1.year_quarter,
    round(100*(t1.revenue - t2.revenue) / t2.revenue, 2) as quarterly_yoy
from
(
    select sum(total_amount) as revenue, year_quarter, year, service_type
    from {{ ref('fact_trips') }}
    where year=2020
    group by year_quarter, year, service_type
) t1
join
(
    select sum(total_amount) as revenue, year_quarter, year, service_type
    from {{ ref('fact_trips') }}
    where year=2019
    group by year_quarter, year, service_type
) t2
on
    t1.service_type = t2.service_type
    and t2.year = t1.year - 1
    and right(t1.year_quarter,2) = right(t2.year_quarter,2)
order by service_type, year_quarter