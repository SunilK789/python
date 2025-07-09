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

# Clean unwanted characters and keep readable values
def extract_clean_text(td):
    text = "".join(td.stripped_strings)
    return re.sub(r'[^\d.,%-]', '', text)

# Format date to dd-MMM-yy (e.g., 14-Jul-25)
def format_date(date_str):
    try:
        parsed = datetime.strptime(date_str.strip(), "%d %b %Y")
        return parsed.strftime("%d-%b-%y")
    except:
        return date_str.strip()

for page in range(1, 2):  # Change to range(1, 11) for 10 pages
    url = base_url.format(page)
    print(f"Fetching page {page}...")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table", class_="data-table")
    if not table:
        print(f"No table found on page {page}")
        continue

    rows = table.find_all("tr")[1:]  # Skip header
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 6:
            # Company name from <a> tag inside first <td>
            name = cols[0].find("a").text.strip() if cols[0].find("a") else cols[0].text.strip()
            list_date = format_date(cols[1].text.strip())

            ipo_data.append({
                "Name": name,
                "List Date": list_date,
                "IPO MCap (Cr)": extract_clean_text(cols[2]),
                "IPO Price": extract_clean_text(cols[3]),
                "Current Price": extract_clean_text(cols[4]),
                "Change %": extract_clean_text(cols[5])
            })

    time.sleep(1)  # Respectful delay

# Save to CSV with timestamp
df = pd.DataFrame(ipo_data)
# Create date-wise folder: D:\IPO Data\YYYY-MM-DD
today_str = datetime.now().strftime("%Y-%m-%d")
base_dir = r"D:\IPO Data"
output_dir = os.path.join(base_dir, today_str)
os.makedirs(output_dir, exist_ok=True)

# Save file to the directory
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = os.path.join(output_dir, f"screener_ipo_data_{timestamp}.csv")
df.to_csv(filename, index=False)
print(f"Saved IPO data to {filename}")

# Auto open the file in default CSV viewer (usually Excel)
subprocess.Popen(['start', '', filename], shell=True)
