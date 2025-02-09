import pandas as pd

def main():
    all_df = []

    months = ["01", "02", "03", "04", "05", "06"]

    for month in months:
        df = pd.read_parquet(f"yellow_tripdata_2024-{month}.parquet")
        all_df.append(df)
    
    merged_df = pd.concat(all_df, ignore_index=True)
    merged_df.to_parquet("yellow_tripdata_2024.parquet", index=False)

if __name__ == '__main__':
    main()