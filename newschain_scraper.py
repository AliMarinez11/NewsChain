import requests
from bs4 import BeautifulSoup
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Headers for web scraping
scrape_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

# News sources
sources = {
    "cnn": {"url": "https://www.cnn.com/politics", "selector": "span.container__headline-text"},
    "fox": {"url": "https://www.foxnews.com/politics", "selector": "h4.title"}
}

# Scrape articles (title, URL, full content)
def scrape_source(source_info):
    url = source_info["url"]
    selector = source_info["selector"]
    source_name = list(sources.keys())[list(sources.values()).index(source_info)]
    try:
        print(f"Fetching main page: {url}")
        response = requests.get(url, headers=scrape_headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        count = 0
        for item in soup.select(selector):
            if count >= 25:  # Revert to 25 articles per source
                break
            title = item.get_text().strip()
            link_elem = item.find_parent('a') or item.find('a')
            if link_elem and 'href' in link_elem.attrs:
                link = link_elem['href']
                # Ensure the correct domain
                if source_name == "fox" and not link.startswith('http'):
                    link = "https://www.foxnews.com" + link
                elif source_name == "cnn" and not link.startswith('http'):
                    link = "https://www.cnn.com" + link
                # Skip video links
                if 'video' in link.lower():
                    print(f"Skipping video link: {link}")
                    continue
                # Scrape the article page for full content
                content = ""
                try:
                    print(f"Fetching article page: {link}")
                    article_response = requests.get(link, headers=scrape_headers, timeout=5)
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    # Collect all paragraphs (adjust selector based on site structure)
                    if source_name == "cnn":
                        paragraphs = article_soup.select('div.article__content p')
                    else:  # fox
                        paragraphs = article_soup.select('div.article-content p')
                    if paragraphs:
                        content = " ".join(p.get_text().strip() for p in paragraphs)
                        if len(content) > 1000:  # Truncate to 1,000 characters if needed
                            content = content[:1000]
                    else:
                        print(f"No content found for {link}")
                        continue
                except Exception as e:
                    print(f"Error scraping content for {link}: {e}")
                    continue
                articles.append({"title": title, "url": link, "source": source_name, "content": content})
                count += 1
        print(f"Scraped {len(articles)} articles from {source_name}")
        # Log the titles of all scraped articles
        print(f"Titles of articles scraped from {source_name}:")
        for article in articles:
            print(f"  - {article['title']}")
        return articles
    except Exception as e:
        print(f"Error scraping {source_name}: {e}")
        return []

# Cluster articles using TF-IDF and cosine similarity
def categorize_articles(articles):
    if not articles:
        print("No articles to cluster")
        return {}

    print(f"Total articles scraped: {len(articles)}")
    print(f"CNN articles: {len([a for a in articles if a['source'] == 'cnn'])}")
    print(f"Fox News articles: {len([a for a in articles if a['source'] == 'fox'])}")

    # Step 1: Prepare the text data (title + content) for TF-IDF
    texts = [f"{article['title']} {article['content']}" for article in articles]

    # Step 2: Convert texts to TF-IDF vectors (for content similarity)
    vectorizer = TfidfVectorizer(stop_words='english', max_df=1.0, min_df=1)
    try:
        X = vectorizer.fit_transform(texts)
        print(f"TF-IDF vectorization successful: {X.shape} matrix (content)")
    except ValueError as e:
        print(f"Error in TF-IDF vectorization (content): {e}")
        return {}

    # Step 3: Separate CNN and Fox News articles
    cnn_articles = [article for article in articles if article['source'] == 'cnn']
    fox_articles = [article for article in articles if article['source'] == 'fox']
    cnn_indices = [i for i, article in enumerate(articles) if article['source'] == 'cnn']
    fox_indices = [i for i, article in enumerate(articles) if article['source'] == 'fox']

    # Step 4: Compute cosine similarity between all CNN and Fox News articles (content)
    similarities = []
    for cnn_idx in cnn_indices:
        for fox_idx in fox_indices:
            similarity = cosine_similarity(X[cnn_idx], X[fox_idx])[0][0]
            if similarity > 0.01:  # Keep threshold at 0.01
                similarities.append((cnn_idx, fox_idx, similarity))

    # Step 5: Sort pairs by similarity and form narratives
    similarities.sort(key=lambda x: x[2], reverse=True)  # Sort by similarity (descending)
    narratives = []
    used_indices = set()  # Track all used indices to prevent duplicates
    for cnn_idx, fox_idx, content_similarity in similarities:
        if cnn_idx in used_indices or fox_idx in used_indices:
            continue  # Skip if either article has already been paired
        cnn_article = articles[cnn_idx]
        fox_article = articles[fox_idx]
        # Extract top 10 keywords from CNN article
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'said', 'trump', 'president', 'that'])
        cnn_text = f"{cnn_article['title']} {cnn_article['content']}"
        cnn_words = re.findall(r'\b\w+\b', cnn_text.lower())
        cnn_keywords = [word for word in cnn_words if word not in stop_words and len(word) > 3]
        cnn_word_counts = {}
        for word in cnn_keywords:
            cnn_word_counts[word] = cnn_word_counts.get(word, 0) + 1
        cnn_top_keywords = sorted(cnn_word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        cnn_top_keywords = [word for word, count in cnn_top_keywords]
        # Extract top 10 keywords from Fox News article
        fox_text = f"{fox_article['title']} {fox_article['content']}"
        fox_words = re.findall(r'\b\w+\b', fox_text.lower())
        fox_keywords = [word for word in fox_words if word not in stop_words and len(word) > 3]
        fox_word_counts = {}
        for word in fox_keywords:
            fox_word_counts[word] = fox_word_counts.get(word, 0) + 1
        fox_top_keywords = sorted(fox_word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        fox_top_keywords = [word for word, count in fox_top_keywords]
        # Check if at least 1 keyword overlaps
        common_keywords = set(cnn_top_keywords).intersection(set(fox_top_keywords))
        if len(common_keywords) < 1:
            print(f"Skipping narrative due to low keyword overlap: {cnn_article['title']} and {fox_article['title']}")
            continue
        
        # Extract top keywords for the category name
        combined_text = f"{cnn_article['title']} {cnn_article['content']} {fox_article['title']} {fox_article['content']}"
        words = re.findall(r'\b\w+\b', combined_text.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        word_counts = {}
        for word in keywords:
            word_counts[word] = word_counts.get(word, 0) + 1
        top_keywords = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:2]
        category_name = " ".join(word.capitalize() for word, count in top_keywords)
        if not category_name:
            # Fallback: Use the first few words of the CNN article title
            category_name = " ".join(cnn_article['title'].split()[:3]).capitalize()
        # Clean up special characters
        category_name = category_name.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
        
        # Form the narrative
        narratives.append({
            "category": category_name,
            "articles": [cnn_article, fox_article]
        })
        used_indices.add(cnn_idx)
        used_indices.add(fox_idx)

    # Step 6: Log the final narratives
    print("Final narratives:")
    for narrative in narratives:
        print(f"Category: {narrative['category']}")
        for article in narrative['articles']:
            print(f"  - {article['source']}: {article['title']}")

    if len(narratives) == 0:
        print("Warning: No narratives found with articles from both sources")

    # Step 7: Format the output as a dictionary
    raw_narratives = {}
    for narrative in narratives:
        raw_narratives[narrative["category"]] = narrative["articles"]

    return raw_narratives

# Main function
def main():
    all_articles = []
    for source_info in sources.values():
        source_name = list(sources.keys())[list(sources.values()).index(source_info)]
        print(f"Scraping {source_name}...")
        articles = scrape_source(source_info)
        all_articles.extend(articles)
    
    # Categorize dynamically
    print("Clustering articles...")
    raw_narratives = categorize_articles(all_articles)
    
    # Save raw data
    raw_path = '/Users/alimarinez/NewsChain/narratives_raw.json'
    with open(raw_path, 'w') as f:
        json.dump(raw_narratives, f, indent=4)
    print(f"Raw narratives saved to {raw_path}")

    # Placeholder for summarization (to be implemented later)
    print("Summarization step skipped for now. Use the raw narratives for inspection.")

if __name__ == "__main__":
    main()
