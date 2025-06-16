import requests
import pandas as pd
import os
import time
from time import sleep
from tqdm import tqdm

API_KEY = "YOUR GOOGLE API KEY"  # ✅ Replace with your API key

keywords = [
    "coffee shop", "shoe repair", "boutique", "local shop",
    "grocery store", "mini mart", "small business store",
    "electronics store", "phone repair", "computer repair",
    "spa", "jewelry store", "watch store"
]

zip_locations = {
    "10128": "40.7813,-73.9507",
    "10075": "40.7736,-73.9566"
}

# === Google Maps Place Search ===
def search_places(query, location, radius, api_key, pagetoken=None):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "location": location,
        "radius": radius,
        "key": api_key
    }
    if pagetoken:
        params["pagetoken"] = pagetoken
        sleep(2)
    return requests.get(url, params=params).json()

def get_place_details(place_id, api_key):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,rating,user_ratings_total",
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json().get("result", {})

# === Main Scraper ===
results = []

for zip_code, location in zip_locations.items():
    for keyword in keywords:
        print(f"🔍 Searching for '{keyword}' in ZIP {zip_code}")
        pagetoken = None
        for _ in range(3):
            data = search_places(keyword, location, 1500, API_KEY, pagetoken)
            places = data.get("results", [])
            for place in tqdm(places, desc=f"{keyword} @ {zip_code}"):
                place_id = place.get("place_id")
                details = get_place_details(place_id, API_KEY)
                results.append({
                    "ZIP": zip_code,
                    "Keyword": keyword,
                    "Business Name": details.get("name", ""),
                    "Address": details.get("formatted_address", ""),
                    "Phone": details.get("formatted_phone_number", ""),
                    "Website": details.get("website", ""),
                    "Rating": details.get("rating", ""),
                    "User Ratings": details.get("user_ratings_total", ""),
                    "Google Maps Link": f"https://www.google.com/maps/place/?q=place_id:{place_id}"
                })
            pagetoken = data.get("next_page_token")
            if not pagetoken:
                break
            sleep(2)

# === Save to CSV ===
df = pd.DataFrame(results)
outfile = "Filtered_Manhattan_Small_Businesses.csv"
df.to_csv(outfile, index=False)
print(f"📁 Data exported to {outfile}")
