### SQL Commands

#### Question 5

```sql
SELECT
  a.service_type,
  a.year_quarter,
  "Best"
FROM
  `kestra-zm.taxi_rides_ny.fct_taxi_trips_quarterly_revenue` a
INNER JOIN (
  SELECT
    service_type,
    MAX(quarterly_yoy) AS best
  FROM
    `kestra-zm.taxi_rides_ny.fct_taxi_trips_quarterly_revenue`
  GROUP BY
    service_type
) b
ON
  a.service_type = b.service_type AND
  a.quarterly_yoy = b.best

UNION ALL

SELECT
  a.service_type,
  a.year_quarter,
  "Worst"
FROM
  `kestra-zm.taxi_rides_ny.fct_taxi_trips_quarterly_revenue` a
INNER JOIN (
  SELECT
    service_type,
    MIN(quarterly_yoy) AS worst
  FROM
    `kestra-zm.taxi_rides_ny.fct_taxi_trips_quarterly_revenue`
  GROUP BY
    service_type
) b
ON
  a.service_type = b.service_type AND
  a.quarterly_yoy = b.worst
```

#### Question 6

```sql
SELECT
  service_type,
  p97,
  p95,
  p90
FROM
  `kestra-zm.taxi_rides_ny.fct_taxi_trips_monthly_fare_p95`
WHERE
  year = 2020 AND
  month = 4
```

#### Question 7

```sql
WITH x as
(
  SELECT * FROM `kestra-zm.taxi_rides_ny.fct_fhv_monthly_zone_traveltime_p90`
  WHERE year = 2019
    AND month = 11
),
a as
(
  SELECT * FROM x
  WHERE pu_zone='Newark Airport'
),
b as
(
  SELECT * FROM x
  WHERE pu_zone='SoHo'
),
c as
(
  SELECT * FROM x
  WHERE pu_zone='Yorkville East'
)
SELECT pu_zone, do_zone
FROM a WHERE p90 = (
  SELECT MAX(p90)
  FROM a WHERE p90 < (
    SELECT MAX(p90)
    FROM a
  )
)
UNION ALL
SELECT pu_zone, do_zone
FROM b WHERE p90 = (
  SELECT MAX(p90)
  FROM b WHERE p90 < (
    SELECT MAX(p90)
    FROM b
  )
)
UNION ALL
SELECT pu_zone, do_zone
FROM c WHERE p90 = (
  SELECT MAX(p90)
  FROM c WHERE p90 < (
    SELECT MAX(p90)
    FROM c
  )
)
```