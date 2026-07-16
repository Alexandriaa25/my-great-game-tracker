#run this: python -m streamlit run app.py

import streamlit as st
import sqlite3
import pandas as pd

# Configure the page layout to be wide and clean
st.set_page_config(page_title="Game Deal Tracker", layout="wide")

# 1. Centered Title and Subtitle
st.markdown("<h1 style='text-align: center;'>🎮 My CheapShark Deal Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Reading live data directly from our SQLite database file.</p>", unsafe_allow_html=True)
st.markdown("---") # Adds a clean horizontal dividing line



# 2. Database Connection
db_connection = sqlite3.connect('game_deals.db')
df = pd.read_sql_query("SELECT display_titles, salePrice, normalPrice, savings, steamRatingPercent FROM best_deals", db_connection)
db_connection.close()

max_price = st.sidebar.slider(
    label="Maximum Price($)",
    min_value= 0.0,
    max_value = 35.99,
    value = 25.00,
    step = 1.00

)

filtered_df = df[df['salePrice'] <= max_price]


# 3. Create a clean 2-column layout for key metrics
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    # Displays a bold card with the total count
    st.metric(label="Deals Tracked", value=len(df))

with metric_col2:
    # Calculate average sale price and display it
    avg_price = df['salePrice'].mean()
    st.metric(label="Average Sale Price", value=f"${avg_price:.2f}")

st.markdown("### 🎯 Live Filtered Game Deals")

# 4. Display the DataFrame beautifully with price formatting
st.dataframe(
    filtered_df.style.format({
        "salePrice": "${:.2f}",
        "normalPrice": "${:.2f}",
        "savings": "${:.2f}"
    }),
    use_container_width=True
)


