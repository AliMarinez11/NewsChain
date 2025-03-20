import requests
from bs4 import BeautifulSoup
import json
import os

# Headers for web scraping
scrape_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

# News sources
sources = {
    "cnn": {"url": "https://www.cnn.com/politics", "selector": "span.container__headline-text"},
    "fox": {"url": "https://www.foxnews.com/politics", "selector": "h4.title"}
}

# Scrape articles
def scrape_source(source_info):
    url = source_info["url"]
    selector = source_info["selector"]
    source_name = list(sources.keys())[list(sources.values()).index(source_info)]
    response = requests.get(url, headers=scrape_headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for item in soup.select(selector):
        title = item.get_text().strip()
        link_elem = item.find_parent('a') or item.find('a')
        if link_elem and 'href' in link_elem.attrs:
            link = link_elem['href']
            if not link.startswith('http'):
                link = "https://www." + source_name + ".com" + link
            articles.append({"title": title, "url": link, "source": source_name})
    return articles

# Categorize articles
def categorize_articles(articles):
    narratives = {}
    for article in articles:
        title = article["title"].lower()
        narrative_key = "other"
        if "trump" in title and "crypto" in title:
            narrative_key = "trump_crypto"
        elif "election" in title:
            narrative_key = "election"
        elif "trump" in title and ("zelenskyy" in title or "putin" in title):
            narrative_key = "trump_zelenskyy_putin"
        if narrative_key not in narratives:
            narratives[narrative_key] = []
        narratives[narrative_key].append(article)
    return narratives

# Main function
def main():
    all_articles = []
    for source_info in sources.values():
        source_name = list(sources.keys())[list(sources.values()).index(source_info)]
        print(f"Scraping {source_name}...")
        articles = scrape_source(source_info)
        all_articles.extend(articles)
    
    # Categorize
    raw_narratives = categorize_articles(all_articles)
    
    # Save raw data
    raw_path = '/Users/alimarinez/NewsChain/narratives_raw.json'
    with open(raw_path, 'w') as f:
        json.dump(raw_narratives, f, indent=4)
    print(f"Raw narratives saved to {raw_path}")

if __name__ == "__main__":
    main()