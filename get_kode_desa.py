import requests
import pandas as pd
import json
from time import perf_counter

# Mulai pencatatan waktu
start_time = perf_counter()
print('Bismillah. Perkiraan berjalan 10 detik. Harap tunggu.')

# Mematikan peringatan SSL
requests.packages.urllib3.disable_warnings() 

# Mengirimkan permintaan dengan session yang sama
s = requests.Session()
r = s.get('https://jaga.id/api/v5/desa/search?limit=1000000&offset=0&nama=&kota=', verify=False)
response_json = r.json()  # Langsung memparsing JSON

# Membuat DataFrame langsung dari data JSON
data_df = pd.DataFrame.from_records(response_json['data']['result'])

# Mengurutkan dan menyimpan ke file CSV
data_df.sort_values(by=['id'], inplace=True)
data_df.to_csv('data_desa_jaga.csv')

# Menghitung waktu dan menampilkan hasil
end_time = perf_counter()
total_time = end_time - start_time
rows = len(data_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")
