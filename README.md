# 🎮 Real-Time Video Game Sale Tracker for Content Creators, Gamers, and More 


A live Streamlit dashboard built to track PC game sales, calculate dollar discounts, and display highly rated discounted games in real time. Save lots of money by checking this dashboard to find games you love!

---

## 💡 About this Project

As a student and YouTube content creator who covers video games, finding affordable games to invest in for my channel is super important to keep things manageable. I built this tool to automate price monitoring so I can quickly identify high-value game deals without manually checking Steam every day.

By querying the CheapShark REST API, this dashboard filters quality games by checking budget conditions and Steam user ratings to find games at the best price point.

---

##  Features
* **Live API Integration:** Gathers real-time price drops directly from the CheapShark REST API.
* **Calculated Savings:** Computes exact dollar savings (`Original Price - Sale Price`) for accurate budgeting.
* **Custom Rating & Price Filters:** Dynamically isolates quality, highly ranked games (85%+ Steam rating) within custom budget ranges.
* **Interactive Dashboard:** Displays top-level key metrics alongside a clean, formatted deal table.

---

## 🛠️ Tech Stack & Architecture

This application is built with **Python**, using **Requests** for live API calls and **Pandas** for data cleaning and metric calculations. The interactive web dashboard is rendered with **Streamlit** and hosted continuously via **Streamlit Community Cloud**.