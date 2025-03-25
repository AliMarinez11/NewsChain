import requests
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
from datetime import datetime, timedelta
from bertopic import BERTopic
from sklearn.metrics.pairwise import cosine_similarity
from newsapi import NewsApiClient  # Import newsapi-python client
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Initialize Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to clean boilerplate text
def clean_boilerplate(text):
    boilerplate_patterns = [
        r"Welcome to the Fox News Politics newsletter, with the latest updates.*?\.\.\.",
        r"Fox News Flash top headlines are here\. Check out what's clicking on Foxnews\.com\.",
        r"A version of this story appeared in CNN’s What Matters newsletter\. To get it in your inbox, sign up for free here\.",
        r"^[A-Za-z\s]+ joins '[A-Za-z\s&]+' to discuss.*?\.",
        r"^[A-Za-z\s]+ told Fox News Digital.*?\."
    ]
    cleaned_text = text
    for pattern in boilerplate_patterns:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.MULTILINE)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

# Function to generate a narrative title based on TF-IDF keywords
def generate_narrative_title(cluster_texts):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(cluster_texts)
    feature_names = vectorizer.get_feature_names_out()
    avg_tfidf = np.mean(tfidf_matrix.toarray(), axis=0)
    top_indices = avg_tfidf.argsort()[-2:][::-1]  # Top 2 keywords
    title = " ".join([feature_names[idx] for idx in top_indices])
    return title

# Function to fetch articles from NewsAPI using newsapi-python
def fetch_articles_from_newsapi(api_key, queries, from_date, to_date, max_articles=500):
    articles = []
    newsapi = NewsApiClient(api_key=api_key)
    for query in queries:
        try:
            # Fetch articles using the /v2/everything endpoint
            response = newsapi.get_everything(
                q=query,
                from_param=from_date,
                to=to_date,
                language='en',
                sort_by='relevancy',
                page_size=100  # Max per page
            )
            if response['status'] != 'ok':
                print(f"Error fetching articles for query '{query}': {response.get('message', 'Unknown error')}")
                continue
            fetched_articles = response['articles']
            for article in fetched_articles:
                # Ensure required fields are present
                if 'title' in article and 'content' in article and 'url' in article:
                    articles.append({
                        "title": article['title'],
                        "content": article['content'] if article['content'] else "",
                        "url": article['url']
                    })
            if len(articles) >= max_articles:
                break
        except Exception as e:
            print(f"Exception fetching articles for query '{query}': {e}")
            continue
    return articles[:max_articles]

# Function to load or fetch articles
def scrape_articles():
    cache_file = 'fetched_articles.json'
    today = datetime.now().strftime('%Y-%m-%d')  # Define today outside the if block
    # Check if cache exists and is from today
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        cache_date = cache_data.get('fetch_date', '')
        if cache_date == today and 'articles' in cache_data and len(cache_data['articles']) > 0:
            print("Loading articles from cache...")
            return cache_data['articles']

    # Fetch new articles if cache is outdated, doesn’t exist, or contains 0 articles
    print("Fetching new articles from NewsAPI...")
    api_key = "f924490a16464459a8566f187a66a58d"  # New NewsAPI key
    queries = ["politics", "technology", "world news", "business", "environment"]
    to_date = "2025-03-24"  # Adjusted to a more recent date
    from_date = "2025-03-01"  # Adjusted to 24 days prior
    articles = fetch_articles_from_newsapi(api_key, queries, from_date, to_date, max_articles=500)

    # Pre-filter articles to exclude non-news content (e.g., privacy notices)
    filtered_articles = []
    non_news_phrases = ['privacy policy', 'terms of service', 'cookie policy', 'accept cookies', 'consent to cookies', 'transparency framework', 'iab']
    for article in articles:
        title = article['title'].lower()
        content = article['content'].lower()
        if not any(phrase in title or phrase in content for phrase in non_news_phrases):
            filtered_articles.append(article)
        else:
            print(f"Excluding article: {article['title']} (likely non-news content)")

    # Cache the filtered articles
    cache_data = {
        "fetch_date": today,
        "articles": filtered_articles
    }
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=4)
    print(f"Fetched and cached {len(filtered_articles)} articles.")
    return filtered_articles

# Main function to scrape and group articles into narratives using clustering
def main():
    # Scrape articles
    raw_articles = scrape_articles()

    # Collect all articles into a flat list and remove duplicates
    all_articles = []
    seen_articles = set()
    for article in raw_articles:
        article_key = (article['title'], article['url'])  # Unique identifier for an article
        if article_key not in seen_articles:
            seen_articles.add(article_key)
            all_articles.append(article)

    print(f"Total articles before filtering: {len(all_articles)}")

    # Clean article content and prepare for clustering
    cleaned_texts = [clean_boilerplate(article['content']) + " " + article['title'] for article in all_articles]
    print(f"Total articles after cleaning: {len(cleaned_texts)}")

    # Compute Sentence-BERT embeddings
    embeddings = model.encode(cleaned_texts, show_progress_bar=True)

    # Use silhouette analysis to determine the optimal number of clusters for K-Means
    best_k = 2
    best_score = -1
    for k in range(2, 31):  # Test K from 2 to 30
        kmeans = KMeans(n_clusters=k, random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings)
        if len(set(cluster_labels)) > 1:  # Need at least 2 clusters for silhouette score
            score = silhouette_score(embeddings, cluster_labels)
            if score > best_score:
                best_score = score
                best_k = k
    print(f"Optimal number of clusters (K): {best_k} with silhouette score: {best_score}")

    # Apply K-Means clustering with the optimal K
    clustering = KMeans(n_clusters=best_k, random_state=42)
    cluster_labels = clustering.fit_predict(embeddings)

    # Group articles by cluster
    clustered_articles = {}
    for idx, label in enumerate(cluster_labels):
        cluster_id = f"Cluster_{label}"
        if cluster_id not in clustered_articles:
            clustered_articles[cluster_id] = []
        clustered_articles[cluster_id].append(all_articles[idx])

    # Apply BERTopic to identify topics for each cluster
    topic_model = BERTopic(embedding_model=model, min_topic_size=2, verbose=True)
    topics, _ = topic_model.fit_transform(cleaned_texts, embeddings=embeddings)

    # Map BERTopic topics to K-Means clusters
    cluster_to_topic = {}
    for idx, label in enumerate(cluster_labels):
        cluster_id = f"Cluster_{label}"
        if cluster_id not in cluster_to_topic:
            cluster_to_topic[cluster_id] = []
        cluster_to_topic[cluster_id].append(topics[idx])

    # Form narratives from clusters, ensuring at least 2 articles per narrative
    filtered_narratives = {}
    for cluster_id, articles in clustered_articles.items():
        print(f"{cluster_id} size: {len(articles)} articles")
        if len(articles) < 2:
            continue  # Skip clusters with fewer than 2 articles

        # Generate a narrative title based on the cluster content
        cluster_texts = [clean_boilerplate(article['content']) + " " + article['title'] for article in articles]
        narrative_title = generate_narrative_title(cluster_texts)
        print(f"{cluster_id} generated title: {narrative_title}")

        # Get the most common BERTopic topic for this cluster
        cluster_topics = cluster_to_topic[cluster_id]
        most_common_topic = max(set(cluster_topics), key=cluster_topics.count, default=-1)
        topic_info = topic_model.get_topic(most_common_topic) if most_common_topic != -1 else []
        topic_keywords = [word for word, _ in topic_info[:5]] if topic_info else []

        filtered_narratives[cluster_id] = {
            "articles": articles,
            "generated_title": narrative_title,
            "topic_keywords": topic_keywords
        }

    # Save the clustered narratives to a separate file
    with open('clustered_narratives.json', 'w') as f:
        json.dump(filtered_narratives, f, indent=4)

    print(f"Collected {len(filtered_narratives)} narratives, saved to clustered_narratives.json")
    return filtered_narratives

if __name__ == "__main__":
    main()