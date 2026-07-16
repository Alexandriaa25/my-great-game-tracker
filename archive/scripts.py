#STEP 1 ... 
#Go to the API with a link. In order for Python to talk to the internet 
#and go to the link, you must import requests.
import requests
data = requests.get('https://www.cheapshark.com/api/1.0/deals?storeID=1&pageSize=10')


#STEP 2 ... transform the data type. Python will get the internet data from
#the API but it needs to be transformed, typically with JSON
#deals now refers to a list of dictionaries
deals = data.json()
 


#STEP 3 ... Once data from API is retrieved and tranformed
# to a readable list or dictionary, loop through it. This will help check 
#for conditions such as prices, locations, ratings, etc.
#we can also do math by subtracting original price to deal price for example!


#deals is the list of dictionaries
#deal is the dictionary in deals

for deal in deals:
    #takes the original values in the dictionary and saves them
    #it also converts them into the needed value, ie a string to a float to
    #operate on.

    #get() is used in case the key does not exist, rather than just deal[key]
    sale_price = float(deal.get('salePrice', 999.0))
    normal_price = float(deal.get('normalPrice', 999.0))
    rating = int(deal.get('steamRatingPercent', 0))
    title = deal.get('title', 'Unknown Game')

   
    savings = normal_price - sale_price

   
    is_good_price = (sale_price < 25.00 or savings > 10.00)
    is_high_quality = (rating > 85)

    if is_good_price and is_high_quality:
        print(f"Don't miss it, {title} is a steal!")