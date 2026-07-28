#run this: python -m streamlit run app.py
import requests
import streamlit as st
import sqlite3
import pandas as pd


st.set_page_config(page_title="Game Deal Tracker", layout="wide")

# put the title/center it 
st.markdown("<h1 style='text-align: center;'> 🎮 Video Game Deal Tracker 🎮</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Monitoring real-time video game sales using the CheapShark REST API! 🦈💛</p>", unsafe_allow_html=True)
st.markdown("---") # Add a chorizontal dividing line



#with sqlite db file
#db_connection = sqlite3.connect('game_deals.db')
#df = pd.read_sql_query("SELECT display_titles, salePrice, normalPrice, savings, steamRatingPercent FROM best_deals", db_connection)
#db_connection.close()


#with live data from cheapshark 
@st.cache_data(ttl=3600)
def fetch_live_deals():
    api_url = "https://www.cheapshark.com/api/1.0/deals?storeID=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        plain_df = pd.DataFrame(data)

        # 1. Convert to numbers
        plain_df["salePrice"] = pd.to_numeric(plain_df["salePrice"])
        plain_df["normalPrice"] = pd.to_numeric(plain_df["normalPrice"])
        plain_df["savings"] = pd.to_numeric(plain_df["savings"])
        plain_df["steamRatingPercent"] = pd.to_numeric(plain_df["steamRatingPercent"])

        # 2. Calculate dollar savings AFTER converting
        plain_df["dollar_savings"] = plain_df["normalPrice"] - plain_df["salePrice"]
        
        # 3. Filter rows
        filtered_deals = plain_df[
            (plain_df["savings"] >= 6.00) & (plain_df["steamRatingPercent"] >= 85)
        ]

        # 4. Trim columns on filtered_deals right before returning
        show = ["title", "salePrice", "normalPrice", "dollar_savings", "steamRatingPercent"]
        filtered_deals = filtered_deals[show]
                
        return filtered_deals

    except Exception as e:
        st.sidebar.error(f"Live deals notice: {e}")
        return pd.DataFrame(columns=["title", "salePrice", "normalPrice", "dollar_savings", "steamRatingPercent"])



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
    filtered_df.rename(columns={
        "title": "Game Title",
        "salePrice": "Sale Price",
        "normalPrice": "Original Price",
        "dollar_savings": "Money saved",
        "steamRatingPercent": "Steam Rating (%)"
    }).style.format({
        "Sale Price": "${:.2f}",
        "Original Price": "${:.2f}",
        "Money saved": "${:.2f}"
    }),
    use_container_width=True
)


