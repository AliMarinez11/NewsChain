import requests
from bs4 import BeautifulSoup
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

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
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(cleaned_texts, show_progress_bar=True)

    # Apply hierarchical clustering
    clustering = AgglomerativeClustering(
        n_clusters=None,  # Let the distance threshold determine the number of clusters
        distance_threshold=0.3,  # Adjust this threshold to control cluster cohesion
        metric='cosine',
        linkage='average'
    )
    cluster_labels = clustering.fit_predict(embeddings)

    # Group articles by cluster
    clustered_articles = {}
    for idx, label in enumerate(cluster_labels):
        cluster_id = f"Cluster_{label}"  # Use cluster IDs instead of predefined names
        if cluster_id not in clustered_articles:
            clustered_articles[cluster_id] = []
        clustered_articles[cluster_id].append(all_articles[idx])

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