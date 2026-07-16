#this will test the data base file made by sqlite

import sqlite3
import pandas as pd

# Connect straight to your permanent database file
conn = sqlite3.connect('game_deals.db')

# Ask SQL to hand over everything from our 'best_deals' table
query = "SELECT gameID, display_titles, salePrice FROM best_deals"
db_df = pd.read_sql_query(query, conn)

# 3. Close the vault door
conn.close()

# 4. Look at what we pulled out of the file!
print("--- FETCHED FROM PERMANENT DATABASE FILE ---")
print(db_df)