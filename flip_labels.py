import pandas as pd

df = pd.read_csv('data/WELFake_Dataset.csv')
df['label'] = 1 - df['label']
df.to_csv('data/WELFake_Dataset.csv', index=False)