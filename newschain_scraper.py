import requests
from bs4 import BeautifulSoup
import json
import os
from collections import Counter
import re

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

# Simple keyword-based clustering for categorization
def categorize_articles(articles):
    if not articles:
        return {}

    # Stop words to ignore
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])

    # Extract keywords from titles
    article_keywords = []
    for article in articles:
        # Tokenize the title: lowercase, remove punctuation, split into words
        title = article["title"].lower()
        words = re.findall(r'\b\w+\b', title)
        # Filter out stop words
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        article_keywords.append((article, keywords))

    # Group articles by shared keywords
    clusters = {}
    used_articles = set()
    cluster_id = 0

    for i, (article, keywords) in enumerate(article_keywords):
        if i in used_articles:
            continue

        # Start a new cluster
        cluster = [article]
        cluster_keywords = set(keywords)
        used_articles.add(i)

        # Look for other articles with overlapping keywords
        for j, (other_article, other_keywords) in enumerate(article_keywords[i+1:], start=i+1):
            if j in used_articles:
                continue
            # Check for at least one shared keyword
            if cluster_keywords.intersection(other_keywords):
                cluster.append(other_article)
                cluster_keywords.update(other_keywords)
                used_articles.add(j)

        # Generate a category name from the top 2 keywords in the cluster
        all_words = []
        for art in cluster:
            words = re.findall(r'\b\w+\b', art["title"].lower())
            all_words.extend([word for word in words if word not in stop_words and len(word) > 3])
        word_counts = Counter(all_words)
        top_words = [word for word, count in word_counts.most_common(2)]
        category_name = "_".join(top_words) if top_words else f"cluster_{cluster_id}"
        clusters[category_name] = cluster
        cluster_id += 1

    # Add remaining articles to an "other" category
    other_articles = [article for i, (article, _) in enumerate(article_keywords) if i not in used_articles]
    if other_articles:
        clusters["other"] = other_articles

    return clusters

# Main function
def main():
    all_articles = []
    for source_info in sources.values():
        source_name = list(sources.keys())[list(sources.values()).index(source_info)]
        print(f"Scraping {source_name}...")
        articles = scrape_source(source_info)
        all_articles.extend(articles)
    
    # Categorize dynamically
    raw_narratives = categorize_articles(all_articles)
    
    # Save raw data
    raw_path = '/Users/alimarinez/NewsChain/narratives_raw.json'
    with open(raw_path, 'w') as f:
        json.dump(raw_narratives, f, indent=4)
    print(f"Raw narratives saved to {raw_path}")
    
    # Call Vercel API with Grok
    vercel_url = "https://news-chain.vercel.app/api/neutralize"
    response = requests.post(vercel_url, json=raw_narratives)
    if response.status_code == 200:
        neutralized_narratives = response.json()
        output_path = '/Users/alimarinez/NewsChain/narratives.json'
        with open(output_path, 'w') as f:
            json.dump(neutralized_narratives, f, indent=4)
        print(f"Neutralized narratives saved to {output_path}")
    else:
        print(f"Vercel API failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()