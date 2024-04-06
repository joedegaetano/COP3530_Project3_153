import pandas as pd

# Read JSON file into DataFrame
df = pd.read_json("yelp_academic_dataset_business.json", lines=True)

# Count the number of records
num_records = len(df)

# Print the number of records
print("Number of records:", num_records)

b_pandas = []
r_dtypes = {"name": str}

with open("yelp_academic_dataset_business.json", "r") as f:
    reader = pd.read_json(f, orient="records", lines=True, dtype=r_dtypes, chunksize=1000)

    for chunk in reader:
        filtered_chunk = chunk[chunk['categories'].str.contains('Restaurants', case=False, na=False)]
        reduced_chunk = filtered_chunk.drop(columns=['business_id', 'hours', 'is_open'])
        b_pandas.append(reduced_chunk)

b_pandas = pd.concat(b_pandas, ignore_index=True)
print(b_pandas)
