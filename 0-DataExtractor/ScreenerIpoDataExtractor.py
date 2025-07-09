import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import re
import os
import subprocess

headers = {
    'User-Agent': 'Mozilla/5.0'
}

base_url = "https://www.screener.in/ipo/recent/?page={}"
ipo_data = []

def extract_clean_text(td):
    text = "".join(td.stripped_strings)
    return re.sub(r'[^\d.,%-]', '', text)

def format_date(date_str):
    try:
        parsed = datetime.strptime(date_str.strip(), "%d %b %Y")
        return parsed.strftime("%d-%b-%y")
    except:
        return date_str.strip()

for page in range(1, 11):  # Pages 1 to 10
    url = base_url.format(page)
    print(f"Fetching page {page}...")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="data-table")
    if not table:
        print(f"No table found on page {page}")
        continue

    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 6:
            name = cols[0].find("a").text.strip() if cols[0].find("a") else cols[0].text.strip()
            list_date = format_date(cols[1].text.strip())
            ipo_price_str = extract_clean_text(cols[3])
            current_price_str = extract_clean_text(cols[4])

            if not ipo_price_str or not current_price_str:
                continue

            try:
                ipo_price = float(ipo_price_str.replace(',', ''))
                current_price = float(current_price_str.replace(',', ''))
            except ValueError:
                continue

            ipo_data.append({
                "Name": name,
                "List Date": list_date,
                "IPO MCap (Cr)": extract_clean_text(cols[2]),
                "IPO Price": ipo_price_str,
                "Current Price": current_price_str,
                "Change %": extract_clean_text(cols[5]),
                "IPO Price Float": ipo_price,
                "Current Price Float": current_price
            })

    time.sleep(1)

# Prepare output paths
today_str = datetime.now().strftime("%Y-%m-%d")
base_dir = r"D:\IPO Data"
output_dir = os.path.join(base_dir, today_str)
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Convert to DataFrame
df = pd.DataFrame(ipo_data)

# Save all data
full_filename = os.path.join(output_dir, f"screener_ipo_data_{timestamp}.csv")
df.drop(columns=["IPO Price Float", "Current Price Float"]).to_csv(full_filename, index=False)
print(f"Saved all IPO data to {full_filename}")

# Filter: Current Price ≥ 1.5 × IPO Price
filtered_df = df[df["Current Price Float"] >= 1.5 * df["IPO Price Float"]].copy()
filtered_df.drop(columns=["IPO Price Float", "Current Price Float"], inplace=True)

# Save filtered data
filtered_filename = os.path.join(output_dir, f"ipo_filtered_data_{timestamp}.csv")
filtered_df.to_csv(filtered_filename, index=False)
print(f"Saved filtered IPO data to {filtered_filename}")

# Open both files
subprocess.Popen(['start', '', full_filename], shell=True)
subprocess.Popen(['start', '', filtered_filename], shell=True)
