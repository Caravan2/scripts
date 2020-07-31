import pandas as pd

filename = "popular_jobs"

df_json = pd.read_json(f'{filename}.json', lines=True)
df_json.to_excel(f'{filename}.xlsx')