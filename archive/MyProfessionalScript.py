# The same as myscript but with functions
import requests
import pandas as pd
import sqlite3

#steps: Extract, transform, load
#Gather the data, type cast, clean it, filer it (keep in mind fall back)



#gather it
def extract_raw_deals():
    url = 'https://www.cheapshark.com/api/1.0/deals?storeID=1&pageSize=65'
    
    try:
        print("Now connecting to CheapShark API...")
        # same as myscript but with a timeout condition. After 15 seconds it will fail
        deals = requests.get(url, timeout=15) 
        
        
        # This line forces an error if the website returns a bad server code (like a 404 or 500 error)
        deals.raise_for_status() 
        
        # If everything went perfectly, return the JSON data
        return deals.json()
        

    except Exception as e:
        # If the internet dies or the site is down, this block runs instead of crashing!
        print(f" API Extraction failed! The error was: {e}")
        return [] # Return an empty list so the rest of the script doesn't break




#type cast with a schema
def transform_deal_data(deals):
    # If the extraction step failed and gave us an empty list, stop immediately
    if not deals:
        return pd.DataFrame()



    # --- YOUR EXACT CLEANING LOGIC GOES HERE ---
    COMPANY_SCHEMA = {
        'title': 'Unknown Game',
        'normalPrice': '0.0',
        'salePrice': '0.0',
        'steamRatingPercent': '0',
        'metacriticScore': '100',
        'gameID': '0'
    }
    
    cleaned_deals = [{key: deal.get(key, default) for key, default in COMPANY_SCHEMA.items()} for deal in deals]
    df = pd.DataFrame(cleaned_deals)
    
    
    # type changes!
    new_dict = {
        'normalPrice' : float,
        'salePrice' : float,
        'steamRatingPercent' : int,
        'metacriticScore' : int,
        'gameID' : int
    }

    df = df.astype(new_dict)

    # then strip of whitespace and other things, create a new column
    # fill any missing values with unknowns and strip. display titles and search titles for data purposes (lowercased)
    df['display_titles'] = df['title'].fillna('unknown').str.strip()
    df['search_titles']  = df['title'].fillna('unknown').str.strip().str.lower()
    df = df.drop(columns=['title'])

    # get all string columns and strip white space, number columns fillna
    string_headers = df.select_dtypes(include=['object', 'string']).columns
    for col in string_headers:
        df[col] = df[col].fillna('unknown').str.strip()

    # calculate savings math track
    df['savings'] = df['normalPrice'] - df['salePrice']
    
    # bouncer filtering rules
    is_good_price = (df['savings'] > 6.00) | (df['salePrice'] < 35.99)
    is_good_game = (df['steamRatingPercent'] >= 85)
    filter_condition = is_good_price & is_good_game
    
    # select our final reporting schema columns
    df = df[['gameID', 'display_titles', 'search_titles', 'normalPrice', 'salePrice', 'savings', 'steamRatingPercent']]
    
    # slice the data down to only records that pass the filters
    filtered_df = df[filter_condition]
    
    #  PRINT FIRST (Before exiting the function)
    print("\n---  LIVE FILTERED GAME DEALS ---")
    print(filtered_df[['display_titles', 'salePrice']])
    
    # THEN EXIT 
    # Instead of just printing it, we "return" the clean DataFrame so the database can use it
    return filtered_df

def load_to_warehouse(filtered_df):
    """Saves the data out of memory into permanent local storage."""
    db_connection = sqlite3.connect('game_deals.db')
    filtered_df.to_sql(name='best_deals', con=db_connection, if_exists='replace', index=False)
    db_connection.close()
    print("\nDatabase Load Complete! Data safely persisted to game_deals.db")

# ─── THE EXECUTION GATE ───
if __name__ == "__main__":
    raw_payload = extract_raw_deals()
    final_clean_df = transform_deal_data(raw_payload)
    load_to_warehouse(final_clean_df)