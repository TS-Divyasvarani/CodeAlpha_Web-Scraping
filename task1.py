# Step 0: Install required libraries
# pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ---------------------------
# 1. Identify and collect data
# ---------------------------

base_url = 'http://quotes.toscrape.com/page/{}/'
all_quotes = []

for page in range(1, 11):  # The site has 10 pages
    url = base_url.format(page)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}")
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # ---------------------------
    # 2. Handle HTML structure
    # ---------------------------
    quotes = soup.find_all('div', class_='quote')
    
    for quote in quotes:
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
        
        # ---------------------------
        # 3. Collect relevant datasets
        # ---------------------------
        all_quotes.append({
            'Quote': text,
            'Author': author,
            'Tags': ', '.join(tags)  # Join multiple tags as comma-separated
        })
    
    # Be polite, avoid overloading server
    time.sleep(1)

# ---------------------------
# 4. Clean & structure data
# ---------------------------

df = pd.DataFrame(all_quotes)
df['Quote'] = df['Quote'].str.replace('“|”', '')  # remove fancy quotes
df['Author'] = df['Author'].str.strip()
df['Tags'] = df['Tags'].str.strip()

# ---------------------------
# 5. Save custom dataset
# ---------------------------

df.to_csv('quotes_dataset.csv', index=False)
print("Dataset saved as 'quotes_dataset.csv'")
print(df.head())
