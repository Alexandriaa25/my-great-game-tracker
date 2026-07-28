#run this: python -m streamlit run app.py
import requests
import streamlit as st
import sqlite3
import pandas as pd


st.set_page_config(page_title="Game Deal Tracker", layout="wide")

# put the title/center it 
st.markdown("<h1 style='text-align: center;'> 🎮 Video Game Sale Tracker 🎮 </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Fetching real-time video game promotions via the CheapShark REST API.</p>", unsafe_allow_html=True)
st.markdown("---") # Add a chorizontal dividing line




#db_connection = sqlite3.connect('game_deals.db')
#df = pd.read_sql_query("SELECT display_titles, salePrice, normalPrice, savings, steamRatingPercent FROM best_deals", db_connection)
#db_connection.close()


#get the deals live from cheapshark
@st.cache_data(ttl=3600)
def fetch_live_deals():
    api_url = "https://www.cheapshark.com/api/1.0/deals?storeID=1"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(api_url, headers=headers, timeout=15)
        
       
        response.raise_for_status()
        
        data = response.json()

        plain_df = pd.DataFrame(data)
        
        

        plain_df["salePrice"] = pd.to_numeric(plain_df["salePrice"])
        plain_df["normalPrice"] = pd.to_numeric(plain_df["normalPrice"])
        plain_df["savings"] = pd.to_numeric(plain_df["savings"])
        plain_df["steamRatingPercent"] = pd.to_numeric(plain_df["steamRatingPercent"])
        
        filtered_deals = plain_df[
            (plain_df["savings"] >= 6.00) & (plain_df["steamRatingPercent"] >= 85)
            ]



        return filtered_deals

    except Exception as e:
        # If something goes wrong (no internet, api down, timeout etc) stop
        st.sidebar.error(" Sorry! Live deals are currently unavailable")
        
        # Return an empty df so the rest doesn't crash
        return pd.DataFrame(columns=["title", "salePrice", "normalPrice", "savings", "steamRatingPercent"])


df = fetch_live_deals()


max_price = st.sidebar.slider(
    label="Maximum Price($)",
    min_value= 0.0,
    max_value = 35.99,
    value = 25.00,
    step = 1.00

)

filtered_df = df[df['salePrice'] <= max_price]



metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric(label="Deals Tracked", value=len(df))

with metric_col2:
    # Calculate average sale price and display it
    avg_price = df['salePrice'].mean()
    st.metric(label="Average Sale Price", value=f"${avg_price:.2f}")

st.markdown("###  Live Filtered Game Deals")

#  Display the DataFrame with price formatting
st.dataframe(
    filtered_df.style.format({
        "salePrice": "${:.2f}",
        "normalPrice": "${:.2f}",
        "savings": "${:.2f}"
    }),
    use_container_width=True
)


