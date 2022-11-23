''' scrape discogs release page for seller ids '''
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

df = pd.read_html('https://www.discogs.com/sell/release/7068875?ev=rb')

# explore
# print("type", type(df))
# print("len", len(df))

# df[0] is the tracklist

# print("columns", df[1].columns)
# print(df[1])

# get the seller's name
print(df[1]['Seller'][1].split()[1])
