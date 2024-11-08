import requests
requests.packages.urllib3.disable_warnings() 
from bs4 import BeautifulSoup
import pandas as pd
import json
from time import perf_counter
start_time = perf_counter()
print('Bismillah. Perkiraan berjalan 11 menit. Harap tunggu.')
s = requests.Session()
r = s.get('https://jaga.id/api/v5/desa/search?limit=1000000&offset=0&nama=&kota=', verify=False)
response_json = json.loads(r.text)
data_df = pd.DataFrame()
for i in response_json['data']['result']:
    row_df = pd.DataFrame(i, index=[0])
    data_df = pd.concat([data_df, row_df], ignore_index=True)
data_df.sort_values(by=['id'])
data_df.to_csv('data_desa_jaga.csv', index=False)
end_time = perf_counter()
total_time = end_time - start_time
rows = len(data_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")
