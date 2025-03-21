import requests
from bs4 import BeautifulSoup
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

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

# Categorize articles dynamically using clustering
def categorize_articles(articles):
    if not articles:
        return {}

    # Extract titles for clustering
    titles = [article["title"] for article in articles]

    # Convert titles to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(titles)
    feature_names = vectorizer.get_feature_names_out()

    # Determine the number of clusters (e.g., square root of the number of articles)
    num_clusters = min(int(len(articles) ** 0.5), len(articles))
    num_clusters = max(2, num_clusters)  # Ensure at least 2 clusters if possible

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)
    labels = kmeans.labels_

    # Group articles by cluster
    clusters = {}
    for i, (article, label) in enumerate(zip(articles, labels)):
        cluster_id = f"cluster_{label}"
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(article)

    # Generate meaningful category names based on most frequent words in each cluster
    narratives = {}
    for label, cluster_articles in clusters.items():
        # Extract all titles in this cluster
        cluster_titles = [article["title"] for article in cluster_articles]
        # Convert to TF-IDF vectors again to find top words
        cluster_X = vectorizer.transform(cluster_titles)
        # Sum the TF-IDF scores for each word across all titles in the cluster
        word_scores = cluster_X.sum(axis=0).A1
        # Get the indices of the top 2 words
        top_word_indices = word_scores.argsort()[-2:][::-1]
        # Get the top 2 words
        top_words = [feature_names[idx] for idx in top_word_indices]
        # Create a category name from the top words
        category_name = "_".join(top_words).lower()
        narratives[category_name] = cluster_articles

    return narratives

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