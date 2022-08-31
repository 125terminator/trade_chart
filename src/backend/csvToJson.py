import pandas as pd
df = pd.read_csv('../../data/reliance.csv')
df.to_json('temp.json', orient='records', lines=True)
