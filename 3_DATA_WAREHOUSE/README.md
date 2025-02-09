Create external table referring to gcs path:

```sql
CREATE OR REPLACE EXTERNAL TABLE `kestra-zm.zoomcamp.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://kestra-zm-448523-bucket/yellow_tripdata_2024.parquet']
);
```

Create a non partitioned table from external table:

```sql
CREATE OR REPLACE TABLE kestra-zm.zoomcamp.yellow_tripdata_2024_non_partitioned AS
SELECT * FROM kestra-zm.zoomcamp.external_yellow_tripdata_2024;
```

#### Question 1

```sql
SELECT
  COUNT(*)
FROM
  kestra-zm.zoomcamp.yellow_tripdata_2024_non_partitioned;
```

#### Question 2

```sql
SELECT
  COUNT(DISTINCT(PULocationID))
FROM
  kestra-zm.zoomcamp.yellow_tripdata_2024_non_partitioned;
```

```sql
SELECT
  COUNT(DISTINCT(PULocationID))
FROM
  kestra-zm.zoomcamp.external_yellow_tripdata_2024;
```

#### Question 3

```sql
SELECT
  PULocationID
FROM
  kestra-zm.zoomcamp.yellow_tripdata_2024_non_partitioned;
```

```sql
SELECT
  PULocationID, DOLocationID
FROM
  kestra-zm.zoomcamp.yellow_tripdata_2024_non_partitioned;
```

#### Question 4

```sql
SELECT
  COUNT(fare_amount)
FROM
  kestra-zm.zoomcamp.yellow_tripdata_2024_non_partitioned
WHERE
  fare_amount = 0
```

#### Question 5

```sql
CREATE OR REPLACE TABLE kestra-zm.zoomcamp.yellow_tripdata_2024_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM kestra-zm.zoomcamp.external_yellow_tripdata_2024;
```

### Question 6

```sql
SELECT DISTINCT(VendorID) FROM kestra-zm.zoomcamp.yellow_tripdata_2024_partitioned_clustered
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```