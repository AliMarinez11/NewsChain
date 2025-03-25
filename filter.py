import json
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Initialize NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

def compute_similarity(article1, article2):
    processed_texts = [preprocess_text(article1), preprocess_text(article2)]
    embeddings = model.encode(processed_texts)
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return similarity

def compute_keyword_overlap(article1, article2):
    tokens1 = set(word_tokenize(preprocess_text(article1)))
    tokens2 = set(word_tokenize(preprocess_text(article2)))
    common_tokens = tokens1.intersection(tokens2)
    overlap = len(common_tokens) / min(len(tokens1), len(tokens2)) if min(len(tokens1), len(tokens2)) > 0 else 0
    return overlap, common_tokens

def filter_narratives(raw_narratives):
    result = {"validNarratives": {}, "excludedNarratives": {}}

    for cluster_id, cluster_data in raw_narratives.items():
        articles = cluster_data["articles"]
        generated_title = cluster_data["generated_title"]
        print(f"\nProcessing cluster: {cluster_id} (Title: {generated_title})")
        if len(articles) < 2:
            result["excludedNarratives"][cluster_id] = {"reason": "Less than 2 articles in the narrative."}
            continue

        article_texts = [article["content"] for article in articles]
        similarity = compute_similarity(article_texts[0], article_texts[1])
        overlap, common_tokens = compute_keyword_overlap(article_texts[0], article_texts[1])
        print(f"Similarity for {cluster_id}: {similarity:.2f}")
        print(f"Keyword overlap for {cluster_id}: {overlap:.2f}, Common tokens: {list(common_tokens)[:10]}")

        # Pass only if similarity is above 0.4 (lowered from 0.5) and keyword overlap is above 0.05 (lowered from 0.1)
        if similarity < 0.4:
            result["excludedNarratives"][cluster_id] = {
                "reason": f"Articles do not share the same general subject (Similarity: {similarity:.2f}).",
                "common_tokens": list(common_tokens)[:10]
            }
            continue
        if overlap < 0.05:
            result["excludedNarratives"][cluster_id] = {
                "reason": f"Insufficient keyword overlap (Overlap: {overlap:.2f}).",
                "common_tokens": list(common_tokens)[:10]
            }
            continue

        result["validNarratives"][cluster_id] = {
            "articles": articles,
            "generated_title": generated_title
        }

    return result

# Load clustered narratives
with open('clustered_narratives.json', 'r') as f:
    raw_narratives = json.load(f)

# Filter narratives
filtered_result = filter_narratives(raw_narratives)

# Save filtered narratives
with open('filtered_narratives.json', 'w') as f:
    json.dump(filtered_result, f, indent=4)

print("Filtered narratives saved to filtered_narratives.json")