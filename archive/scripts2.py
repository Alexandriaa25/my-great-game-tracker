#WELCOME to the more advanced stage! ... now we will import pandas.
#This is to transform the basic dictionary into like a spreadsheet 
# within the code
import requests
import pandas as pd

#use this to see everything:  
# pd.set_option('display.max_columns', None)


#use same api and dictionaries as scripts1
data = requests.get('https://www.cheapshark.com/api/1.0/deals?storeID=1&pageSize=10') 


#convert the unreadable string from the internet into a list of dicts
deals = data.json()

#before passing to pandas, lets clean up and make sure things exist
#heres onee way to clean them


#here is one (slow) way
#COMMENT OUT BEFORE RUNNING
'''
cleaned_deals = [
    {
        'title': deal.get('title', 'Unknown Game'),
        'normalPrice': deal.get('normalPrice', '0.0'),
        'salePrice': deal.get('salePrice', '0.0'),
        'steamRatingPercent': deal.get('steamRatingPercent', '0')
    }
    for deal in deals
]
'''


#A BETTER WAY
COMPANY_SCHEMA = {
    'title': 'Unknown Game',
    'normalPrice': '0.0',
    'salePrice': '0.0',
    'steamRatingPercent': '0',
    'metacriticScore': '100',
    'gameID': '0'
}

#heres a better way (given a company schema)
cleaned_deals = [
    {key: deal.get(key, default) for key, default in COMPANY_SCHEMA.items()}
    for deal in deals
]



#transform deals dictionaries into a pandas spreadsheet
df = pd.DataFrame(cleaned_deals)


#next we need to clean more by clearing out undeeded colums, and converting data types.
#we want game title, original price, sale price, rating. Nothing else for now! 
#make sure to convert/calculate these first



#this step creates a list of only the labels we want, and passes it into df brackets
#df = df[['title','normalPrice','salePrice','steamRatingPercent', 'metacriticScore']]

# Tell Pandas exactly which columns to keep, and what order to display them in!




#to do this in a scalable way, pass a dictionary into astype instead of manually
#typing and saving

new_dict = {

    'normalPrice' : float,
    'salePrice' : float,
    'steamRatingPercent' : int,
    'metacriticScore' : int,
    'gameID' : int

}

#we passed the new_dict to use astype all at once, instead of manually
#assining like price = float(normalPrice)
df = df.astype(new_dict)


#before operations and now that we have clean, typed dataframe. Lets strip any
#uneeded trailing whitespace. In a corporate setting with lots of data
#its to slow to manually .strip each string column. Use the following to get all of them


#object refers to strings, so its selecting only those
# 1. First, create your two separate title tracks explicitly from the original column
df['display_titles'] = df['title'].fillna('unknown').str.strip()
df['search_titles']  = df['title'].fillna('unknown').str.strip().str.lower()



# 2. Now, drop the original messy 'title' column so it's not duplicated
df = df.drop(columns=['title'])



# let your automated loops catch any OTHER text or number columns
string_headers = df.select_dtypes(include=['object', 'string']).columns

for col in string_headers:
    # Since we already polished display_titles and search_titles, 
    # this loop will safely skip over them or just re-verify them without breaking anything!
    df[col] = df[col].fillna('unknown').str.strip()


# Tell Pandas exactly which columns to keep, and what order to display them in!




#same but for numbers (if there is a non existant value, safely replace with 0 instead of crashing)
numeric_headers = df.select_dtypes(include=['number']).columns
for col in numeric_headers:
    df[col] = df[col].fillna(0)




# This creates a brand new column named 'savings' populated by the math
#its almost like excel in Python
df['savings'] = df['normalPrice'] - df['salePrice']




is_good_price = (df['savings'] > 10.00) | (df['salePrice'] < 25.99)
is_good_game = (df['steamRatingPercent'] >= 85)




filter = is_good_price & is_good_game



#pass filter to data frame, check which rows meet the conditions and keep them
filtered_df = df[filter]


# Tell Pandas exactly which columns to keep, and what order to display them in!
df = df[['gameID', 'display_titles', 'search_titles', 'normalPrice', 'salePrice', 'savings', 'steamRatingPercent']]



#print the titles of the data in the frame that passes the filter
print(filtered_df['display_titles'])



#IF STATEMENTS DO NOT WORK WITH PANDAS TABLES
#why? there are many rows with different values which cannot have a unanimous t/f value
