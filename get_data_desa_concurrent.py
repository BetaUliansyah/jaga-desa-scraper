import requests
requests.packages.urllib3.disable_warnings() 
import pandas as pd
import json
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor, as_completed

start_time = perf_counter()

# Initialize session
s = requests.Session()
tahun = 2024

# Read kode_desa data
desa_df = pd.read_csv('data_desa_jaga.csv', index_col=0)
kode_desa_list = desa_df['id'].head(500)

# Function to fetch data for a single kode_desa
def fetch_data(kode_desa):
    try:
        url = f'https://jaga.id/api/v5/desa/summary/{kode_desa}/{tahun}?anggaranKumulatif=1'
        response = s.get(url, verify=False)
        response_json = response.json()
        return response_json['data']  # Return dictionary
    except Exception as e:
        print(f"Failed to fetch data for kode_desa {kode_desa}: {e}")
        return None  # Return None on failure

# Collect data as a list of dictionaries
data_list = []

# Use ThreadPoolExecutor for concurrent requests
with ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(fetch_data, kode_desa): kode_desa for kode_desa in kode_desa_list}
    for future in as_completed(futures):
        result = future.result()
        if result:
            data_list.append(result)

# Create a DataFrame from list of dictionaries
data_df = pd.DataFrame(data_list)

# Save the results to CSV
data_df.to_csv('data-desa-concurrent.csv', index=False)

# Print elapsed time
end_time = perf_counter()
total_time = end_time - start_time
rows = len(data_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")
