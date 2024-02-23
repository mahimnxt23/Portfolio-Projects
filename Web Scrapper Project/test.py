import pandas as pd

csv_filename = 'curated_news.csv'
df = pd.read_csv(csv_filename)

print(df.head(100))
