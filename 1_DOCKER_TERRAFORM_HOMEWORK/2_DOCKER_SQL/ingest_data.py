#!/usr/bin/env python
# coding: utf-8

from time import time
from sqlalchemy import create_engine
import pandas as pd
import argparse
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    trips_table_name = params.trips_table_name
    zones_table_name = params.zones_table_name
    trips_url = params.trips_url
    zones_url = params.zones_url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if trips_url.endswith('.csv.gz'):
        trips_csv_name = 'trips_output.csv.gz'
    else:
        trips_csv_name = 'trips_output.csv'
    
    if zones_url.endswith('.csv.gz'):
        zones_csv_name = 'zones_output.csv.gz'
    else:
        zones_csv_name = 'zones_output.csv'

    print(trips_csv_name)
    print(zones_csv_name)

    os.system(f"wget {trips_url} -O {trips_csv_name}")
    os.system(f"wget {zones_url} -O {zones_csv_name}")

    # download the csv

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    trips_df_iter = pd.read_csv(trips_csv_name, iterator=True, chunksize=100000)

    trips_df = next(trips_df_iter)

    trips_df.lpep_pickup_datetime = pd.to_datetime(trips_df.lpep_pickup_datetime)
    trips_df.lpep_dropoff_datetime = pd.to_datetime(trips_df.lpep_dropoff_datetime)

    trips_df.head(n=0).to_sql(name=trips_table_name, con=engine, if_exists='replace')

    trips_df.to_sql(name=trips_table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()

            trips_df = next(trips_df_iter)

            trips_df.lpep_pickup_datetime = pd.to_datetime(trips_df.lpep_pickup_datetime)
            trips_df.lpep_dropoff_datetime = pd.to_datetime(trips_df.lpep_dropoff_datetime)

            trips_df.to_sql(name=trips_table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk..., took %.3f seconds' % (t_end - t_start))
        
        except:
            print("Finished ingesting data into the postgres database")
            break
    
    zones_df = pd.read_csv(zones_csv_name)
    zones_df.head(n=0).to_sql(name=zones_table_name, con=engine, if_exists='replace')
    zones_df.to_sql(name=zones_table_name, con=engine, if_exists='append')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--trips_table_name', help='name of the trips table where we will write the results to')
    parser.add_argument('--zones_table_name', help='name of the zones table where we will write the results to')
    parser.add_argument('--trips_url', help='url of the trips csv file')
    parser.add_argument('--zones_url', help='url of the zones csv file')

    args = parser.parse_args()

    main(args)