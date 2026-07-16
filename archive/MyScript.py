#here is the cleaned version of advanced script2
import requests
import pandas as pd
import sqlite3 


data = requests.get('https://www.cheapshark.com/api/1.0/deals?storeID=1&pageSize=30') 
deals = data.json()


COMPANY_SCHEMA = {
    'title': 'Unknown Game',
    'normalPrice': '0.0',
    'salePrice': '0.0',
    'steamRatingPercent': '0',
    'metacriticScore': '100',
    'gameID': '0'
}


cleaned_deals = [
    {key: deal.get(key, default) for key, default in COMPANY_SCHEMA.items()}
    for deal in deals
]



df = pd.DataFrame(cleaned_deals)



new_dict = {
    'normalPrice' : float,
    'salePrice' : float,
    'steamRatingPercent' : int,
    'metacriticScore' : int,
    'gameID' : int
}


df = df.astype(new_dict)


df['display_titles'] = df['title'].fillna('unknown').str.strip()
df['search_titles']  = df['title'].fillna('unknown').str.strip().str.lower()
df = df.drop(columns=['title'])


#
string_headers = df.select_dtypes(include=['object', 'string']).columns
for col in string_headers:
    df[col] = df[col].fillna('unknown').str.strip()



numeric_headers = df.select_dtypes(include=['number']).columns
for col in numeric_headers:
    df[col] = df[col].fillna(0)

df['savings'] = df['normalPrice'] - df['salePrice']



is_good_price = (df['savings'] > 6.00) | (df['salePrice'] < 35.99)
is_good_game = (df['steamRatingPercent'] >= 85)
filter_condition = is_good_price & is_good_game

df = df[['gameID', 'display_titles', 'search_titles', 'normalPrice', 'salePrice', 'savings', 'steamRatingPercent']]

filtered_df = df[filter_condition]

print("\n--- FINAL FILTERED PORTFOLIO REPORT ---")
print(filtered_df[['display_titles']])



#connect with sqlite make database file
db_connection = sqlite3.connect('game_deals.db')


filtered_df.to_sql(name='best_deals', con=db_connection, if_exists='replace', index=False)


db_connection.close()

print("\n Database Load Complete! Data safely persisted to game_deals.db")