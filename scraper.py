import requests
from bs4 import BeautifulSoup
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import re
import numpy as np

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

# Function to compute TF-IDF similarity between two articles
def compute_tfidf_similarity(article1, article2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([article1, article2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity

# Function to compute average TF-IDF similarity within a cluster
def compute_cluster_similarity(cluster_texts):
    similarities = []
    for i in range(len(cluster_texts)):
        for j in range(i + 1, len(cluster_texts)):
            similarity = compute_tfidf_similarity(cluster_texts[i], cluster_texts[j])
            similarities.append(similarity)
    return sum(similarities) / len(similarities) if similarities else 0

# Function to refine clusters by splitting based on TF-IDF similarity
def refine_clusters(clustered_articles, all_articles, article_to_category):
    refined_clusters = {}
    cluster_id = 0

    for old_cluster_id, articles in clustered_articles.items():
        if len(articles) < 2:
            continue  # Skip clusters with fewer than 2 articles

        # Compute initial cluster similarity
        cluster_texts = [clean_boilerplate(article['content']) + " " + article['title'] for article in articles]
        avg_similarity = compute_cluster_similarity(cluster_texts)
        print(f"Cluster {old_cluster_id} initial average TF-IDF similarity: {avg_similarity:.2f}")

        # If the cluster is cohesive (avg similarity >= 0.15), keep it as is
        if avg_similarity >= 0.15:
            refined_clusters[cluster_id] = articles
            cluster_id += 1
            continue

        # Otherwise, split the cluster into sub-clusters using K-means
        sub_num_clusters = max(int(len(articles) // 2), 1)  # Aim for smaller sub-clusters
        if sub_num_clusters < 2:
            refined_clusters[cluster_id] = articles
            cluster_id += 1
            continue

        # Compute TF-IDF vectors for sub-clustering
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(cluster_texts)
        kmeans = KMeans(n_clusters=sub_num_clusters, random_state=42)
        sub_cluster_labels = kmeans.fit_predict(tfidf_matrix)

        # Group articles by sub-cluster
        sub_clusters = {}
        for idx, label in enumerate(sub_cluster_labels):
            if label not in sub_clusters:
                sub_clusters[label] = []
            sub_clusters[label].append(articles[idx])

        # Add sub-clusters as new clusters if they have at least 2 articles
        for sub_label, sub_articles in sub_clusters.items():
            if len(sub_articles) < 2:
                continue  # Skip sub-clusters with fewer than 2 articles
            sub_cluster_texts = [clean_boilerplate(article['content']) + " " + article['title'] for article in sub_articles]
            sub_avg_similarity = compute_cluster_similarity(sub_cluster_texts)
            print(f"Sub-cluster {cluster_id} (from Cluster {old_cluster_id}) average TF-IDF similarity: {sub_avg_similarity:.2f}")
            if sub_avg_similarity >= 0.05:  # Keep threshold for sub-clusters
                refined_clusters[cluster_id] = sub_articles
                cluster_id += 1

    return refined_clusters, all_articles, article_to_category

# Load existing raw_narratives.json safely
def load_existing_narratives():
    try:
        with open('raw_narratives.json', 'r') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

# Simulated scraper function (replace with actual scraping logic later)
def scrape_articles(search_terms):
    raw_narratives = load_existing_narratives()
    if not raw_narratives:
        print("No valid existing data found, initializing with placeholder data.")
        with open('raw_narratives.json', 'r') as f:
            raw_narratives = json.load(f)
    return raw_narratives

# Main function to scrape and group articles into narratives using clustering
def main():
    # Example search terms (replace with actual search terms)
    search_terms = [
        "Musk Pentagon", "Ukraine Putin", "Department Education", "Boasberg Judge",
        "Canada State", "Biden Former", "King Files", "Government Federal",
        "Democrats Town", "Tesla Musk", "Administration Power", "State Rubio",
        "Walz 2024", "Crisis Been", "First Term", "Maher Food"
    ]

    # Scrape articles
    raw_narratives = scrape_articles(search_terms)

    # Collect all articles into a flat list and remove duplicates
    all_articles = []
    article_to_category = []
    seen_articles = set()
    for category, articles in raw_narratives.items():
        for article in articles:
            article_key = (article['title'], article['url'])  # Unique identifier for an article
            if article_key not in seen_articles:
                seen_articles.add(article_key)
                all_articles.append(article)
                article_to_category.append(category)

    print(f"Total articles before filtering: {len(all_articles)}")

    # Clean article content and prepare for clustering
    cleaned_texts = [clean_boilerplate(article['content']) + " " + article['title'] for article in all_articles]
    print(f"Total articles after cleaning: {len(cleaned_texts)}")

    # Compute TF-IDF vectors for clustering
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_texts)

    # Apply K-means clustering
    num_clusters = max(int(len(cleaned_texts) // 3), 1)  # Keep number of clusters
    print(f"Number of clusters: {num_clusters}")
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)

    # Group articles by cluster
    clustered_articles = {}
    for idx, label in enumerate(cluster_labels):
        if label not in clustered_articles:
            clustered_articles[label] = []
        clustered_articles[label].append(all_articles[idx])

    # Refine clusters
    refined_clusters, all_articles, article_to_category = refine_clusters(clustered_articles, all_articles, article_to_category)

    # Form narratives from refined clusters
    filtered_narratives = {}
    for cluster_id, articles in refined_clusters.items():
        # Use the original category of the first article as the narrative name
        category = article_to_category[all_articles.index(articles[0])]
        filtered_narratives[category] = articles

    # Save the clustered narratives to a separate file
    with open('clustered_narratives.json', 'w') as f:
        json.dump(filtered_narratives, f, indent=4)

    print(f"Collected {len(filtered_narratives)} narratives, saved to clustered_narratives.json")
    return filtered_narratives

if __name__ == "__main__":
    main()