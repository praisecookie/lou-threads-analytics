import pandas as pd
import numpy as np
import json
import random
from datetime import datetime, timedelta

# --- 1. SETUP COLLECTIONS & RULES ---
collections = {
    "Sequels": ["Neon Nights II", "Urban Essentials 2.0", "Denim Days V2", "Summer Breeze Returns"],
    "Originals": ["Cyberpunk Couture", "Eco-Chic Fall", "Lunar Loungewear", "Vintage Vault"]
}

items = ["Leather Jacket", "Graphic T-Shirt",
         "Distressed Jeans", "Sundress", "Beanie"]
base_prices = {"Leather Jacket": 120, "Graphic T-Shirt": 35,
               "Distressed Jeans": 75, "Sundress": 60, "Beanie": 25}

# --- 2. GENERATE HISTORICAL SALES ---
np.random.seed(42)  # For reproducibility
num_orders = 523

sales_data = []
for i in range(num_orders):
    order_id = f"ORD-{1000 + i}"
    category = np.random.choice(["Sequels", "Originals"])
    collection_name = np.random.choice(collections[category])
    item_type = np.random.choice(items)

    # Originals are slightly more expensive, Sequels sell slightly more units per order
    price_multiplier = 1.2 if category == "Originals" else 1.0
    unit_price = round(base_prices[item_type] * price_multiplier, 2)
    units_sold = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1]) if category == "Originals" else np.random.choice(
        [1, 2, 3, 4], p=[0.5, 0.3, 0.15, 0.05])

    total_revenue = unit_price * units_sold

    sales_data.append([order_id, collection_name, item_type,
                      units_sold, unit_price, total_revenue, category[:-1]])

df_sales = pd.DataFrame(sales_data, columns=[
                        "Order_ID", "Collection_Name", "Item_Type", "Units_Sold", "Unit_Price", "Total_Revenue", "Collection_Category"])
df_sales.to_csv("data/historical_sales.csv", index=False)


# --- 3. GENERATE CUSTOMER REVIEWS (Subset of orders) ---
# Not everyone leaves a review, let's say 350 reviews
review_orders = random.sample(sales_data, 350)
reviews_data = []

for order in review_orders:
    order_id = order[0]
    category = order[6]  # "Sequel" or "Original"

    # Logic: Originals are experimental (more returns, wider rating variance). Sequels are safe.
    if category == "Original":
        star_rating = np.random.choice(
            [1, 2, 3, 4, 5], p=[0.1, 0.15, 0.2, 0.3, 0.25])
        returned = np.random.choice(["Yes", "No"], p=[0.25, 0.75])
    else:
        star_rating = np.random.choice([3, 4, 5], p=[0.1, 0.4, 0.5])
        returned = np.random.choice(["Yes", "No"], p=[0.08, 0.92])

    sentiment = "Positive" if star_rating >= 4 else (
        "Neutral" if star_rating == 3 else "Negative")

    reviews_data.append([order_id, star_rating, returned, sentiment])

df_reviews = pd.DataFrame(reviews_data, columns=[
                          "Order_ID", "Star_Rating", "Return_Status", "Sentiment"])
df_reviews.to_csv("data/customer_reviews.csv", index=False)


# --- 4. GENERATE MARKETING SPEND (Excel File) ---
marketing_data = []
all_collections = collections["Sequels"] + collections["Originals"]

for coll in all_collections:
    is_original = coll in collections["Originals"]
    # We spend way more marketing money on new Original collections
    base_spend = 15000 if is_original else 5000

    tiktok = base_spend + np.random.randint(-2000, 5000)
    ig = base_spend + np.random.randint(-1000, 3000)
    google = base_spend + np.random.randint(-3000, 1000)

    total_spend = tiktok + ig + google
    # Roughly $1.50 per click
    clicks = int((total_spend / 1.5) + np.random.randint(1000, 5000))

    marketing_data.append([coll, tiktok, ig, google, total_spend, clicks])

df_marketing = pd.DataFrame(marketing_data, columns=[
                            "Collection_Name", "TikTok_Spend", "IG_Spend", "Google_Ads_Spend", "Total_Spend", "Clicks"])
df_marketing.to_excel("data/marketing_spend.xlsx", index=False)


# --- 5. GENERATE TREND INDEX (JSON File) ---
trend_data = []
for coll in all_collections:
    is_original = coll in collections["Originals"]
    # Originals trend higher socially because they are brand new
    trend_score = np.random.randint(
        75, 98) if is_original else np.random.randint(40, 70)
    trend_data.append(
        {"collection_name": coll, "google_trends_score": trend_score})

with open("data/trend_index.json", "w") as f:
    json.dump(trend_data, f, indent=4)

print("✅ SUCCESS! 4 Datasets generated and saved to the /data folder.")
