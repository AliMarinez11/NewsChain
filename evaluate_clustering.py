import json
import numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import re  # For regular expressions

# Initialize Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to clean boilerplate text (copied from scraper.py for consistency)
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

# Load filtered narratives (pipeline output after filtering)
with open('filtered_narratives.json', 'r') as f:
    filtered_narratives = json.load(f)

# Create predicted labels from filtered narratives
article_to_predicted_label = {}
article_texts = []
article_indices = []
for cluster_id, cluster_data in filtered_narratives['validNarratives'].items():
    for article in cluster_data['articles']:
        article_title = article['title']
        article_to_predicted_label[article_title] = cluster_id
        article_texts.append(clean_boilerplate(article['content']) + " " + article['title'])
        article_indices.append(article_title)

# Compute embeddings for all articles
embeddings = model.encode(article_texts)

# Compute silhouette score and Davies-Bouldin index
if len(set(article_to_predicted_label.values())) > 1:  # Need at least 2 clusters
    labels = [article_to_predicted_label[title] for title in article_indices]
    # Convert labels to integers for metric computation
    label_map = {label: idx for idx, label in enumerate(set(labels))}
    labels_encoded = [label_map[label] for label in labels]
    # Compute distance matrix for silhouette score
    distance_matrix = 1 - cosine_similarity(embeddings)
    np.fill_diagonal(distance_matrix, 0)  # Ensure diagonal is 0
    # Clip negative values to 0 to ensure non-negative distances
    distance_matrix = np.maximum(distance_matrix, 0)
    silhouette = silhouette_score(distance_matrix, labels_encoded, metric='precomputed')
    db_index = davies_bouldin_score(embeddings, labels_encoded)
else:
    silhouette = 0.0
    db_index = float('inf')

# Print results
print("Metrics for clustered articles only:")
print(f"Silhouette Score: {silhouette:.4f}")
print(f"Davies-Bouldin Index: {db_index:.4f}")
print(f"Number of narratives formed: {len(filtered_narratives['validNarratives'])}")

# Print mapping of clusters to generated titles
print("\nCluster to Generated Title Mapping:")
for cluster_id, cluster_data in filtered_narratives['validNarratives'].items():
    print(f"{cluster_id} (Title: {cluster_data['generated_title']})")