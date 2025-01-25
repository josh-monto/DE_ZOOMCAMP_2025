#### Question 1

The following code was run from the terminal:

```shell script
docker run -it --entrypoint=bash python:3.12.8
```

To return the pip version in question, the following bash prompt was then used:

```shell script
pip --version
```
#### Question 2

No code

#### Question 3

To return the number of trips for each distance range:

```sql
SELECT COUNT(*) FROM public.green_taxi_trips
WHERE trip_distance <= 1
```
```sql
SELECT COUNT(*) FROM public.green_taxi_trips
WHERE trip_distance > 1 AND trip_distance <= 3
```
```sql
SELECT COUNT(*) FROM public.green_taxi_trips
WHERE trip_distance > 3 AND trip_distance <= 7
```
```sql
SELECT COUNT(*) FROM public.green_taxi_trips
WHERE trip_distance > 7 AND trip_distance <= 10
```
```sql
SELECT COUNT(*) FROM public.green_taxi_trips
WHERE trip_distance > 10
```

#### Question 4

Query to return pickup date of longest trip distance:

```sql
SELECT TO_CHAR(lpep_pickup_datetime, 'YYYY-MM-DD')
FROM public.green_taxi_trips
ORDER BY trip_distance DESC
LIMIT 1
```

#### Question 5

Query to return only the names of the 3 biggest pickup zones:

```sql
SELECT "Zone" FROM
	(SELECT SUM(total_amount) AS total, "Zone"
	FROM public.green_taxi_trips t
	JOIN zones zpu ON t."PULocationID" = zpu."LocationID"
	WHERE TO_CHAR(lpep_pickup_datetime, 'YYYY-MM-DD') = '2019-10-18'
	GROUP BY "Zone"
	ORDER BY total DESC)
LIMIT 3
```

#### Question 6

Query to return only the name of the drop off zone coming from East Harlem North with the largest tip

```sql
SELECT zdo."Zone"
FROM public.green_taxi_trips t
JOIN zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN zones zdo ON t."DOLocationID" = zdo."LocationID"
WHERE zpu."Zone" = 'East Harlem North'
ORDER BY tip_amount DESC
LIMIT 1
```

#### Question 7

No code
