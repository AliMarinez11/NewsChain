import requests
from bs4 import BeautifulSoup
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Initialize NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
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

# Function to preprocess text for keyword overlap (not used for merging but kept for compatibility)
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

# Function to compute average pairwise similarity between two clusters
def compute_cluster_similarity(cluster_articles1, cluster_articles2):
    # Extract texts from articles in both clusters
    texts1 = [clean_boilerplate(article['content']) + " " + article['title'] for article in cluster_articles1]
    texts2 = [clean_boilerplate(article['content']) + " " + article['title'] for article in cluster_articles2]
    
    # Compute embeddings for all articles
    all_texts = texts1 + texts2
    embeddings = model.encode(all_texts)
    embeddings1 = embeddings[:len(texts1)]
    embeddings2 = embeddings[len(texts1):]
    
    # Compute pairwise similarities between all articles in the two clusters
    similarities = cosine_similarity(embeddings1, embeddings2)
    
    # Return the average similarity
    avg_similarity = np.mean(similarities)
    return avg_similarity

# Function to generate a narrative title based on TF-IDF keywords
def generate_narrative_title(cluster_texts):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(cluster_texts)
    feature_names = vectorizer.get_feature_names_out()
    # Get the top 2 keywords based on TF-IDF scores
    avg_tfidf = np.mean(tfidf_matrix.toarray(), axis=0)
    top_indices = avg_tfidf.argsort()[-2:][::-1]  # Top 2 keywords
    title = " ".join([feature_names[idx] for idx in top_indices])
    return title

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
def scrape_articles():
    raw_narratives = load_existing_narratives()
    if not raw_narratives:
        print("No valid existing data found, initializing with placeholder data.")
        with open('raw_narratives.json', 'r') as f:
            raw_narratives = json.load(f)
    return raw_narratives

# Main function to scrape and group articles into narratives using clustering
def main():
    # Scrape articles
    raw_narratives = scrape_articles()

    # Collect all articles into a flat list and remove duplicates
    all_articles = []
    seen_articles = set()
    for category, articles in raw_narratives.items():
        for article in articles:
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

    # Apply DBSCAN clustering on original embeddings
    clustering = DBSCAN(
        eps=0.4,  # Set to 0.4 as it achieved 9/13 narratives in Iteration 7
        min_samples=2,  # Minimum articles per cluster
        metric='cosine'  # Use cosine distance on original embeddings
    )
    cluster_labels = clustering.fit_predict(embeddings)

    # Group articles by cluster
    initial_clusters = {}
    for idx, label in enumerate(cluster_labels):
        if label == -1:  # DBSCAN labels noise points as -1
            continue  # Skip unclustered articles for now
        cluster_id = f"Cluster_{label}"
        if cluster_id not in initial_clusters:
            initial_clusters[cluster_id] = []
        initial_clusters[cluster_id].append(all_articles[idx])

    # Rule-based merging of clusters based on average pairwise similarity
    merged_clusters = {}
    cluster_ids = list(initial_clusters.keys())
    merged = set()
    merge_threshold = 0.70  # Increased similarity threshold for merging to prevent over-merging

    for i, cluster_id1 in enumerate(cluster_ids):
        if cluster_id1 in merged:
            continue
        merged_cluster = initial_clusters[cluster_id1].copy()
        merged_cluster_id = cluster_id1

        for j, cluster_id2 in enumerate(cluster_ids[i+1:], start=i+1):
            if cluster_id2 in merged:
                continue
            avg_similarity = compute_cluster_similarity(initial_clusters[cluster_id1], initial_clusters[cluster_id2])
            if avg_similarity >= merge_threshold:
                merged_cluster.extend(initial_clusters[cluster_id2])
                merged.add(cluster_id2)

        merged.add(cluster_id1)
        merged_clusters[merged_cluster_id] = merged_cluster

    # Form narratives from merged clusters, ensuring at least 2 articles per narrative
    filtered_narratives = {}
    for cluster_id, articles in merged_clusters.items():
        print(f"{cluster_id} size: {len(articles)} articles")
        if len(articles) < 2:
            continue  # Skip clusters with fewer than 2 articles

        # Generate a narrative title based on the cluster content
        cluster_texts = [clean_boilerplate(article['content']) + " " + article['title'] for article in articles]
        narrative_title = generate_narrative_title(cluster_texts)
        print(f"{cluster_id} generated title: {narrative_title}")

        filtered_narratives[cluster_id] = {
            "articles": articles,
            "generated_title": narrative_title
        }

    # Save the clustered narratives to a separate file
    with open('clustered_narratives.json', 'w') as f:
        json.dump(filtered_narratives, f, indent=4)

    print(f"Collected {len(filtered_narratives)} narratives, saved to clustered_narratives.json")
    return filtered_narratives

if __name__ == "__main__":
    main()