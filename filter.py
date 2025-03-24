import json
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
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
tfidf_vectorizer = TfidfVectorizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

def compute_tfidf_similarity(article1, article2):
    processed_texts = [preprocess_text(article1), preprocess_text(article2)]
    tfidf_matrix = tfidf_vectorizer.fit_transform(processed_texts)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity

def compute_keyword_overlap(article1, article2):
    tokens1 = set(word_tokenize(preprocess_text(article1)))
    tokens2 = set(word_tokenize(preprocess_text(article2)))
    common_tokens = tokens1.intersection(tokens2)
    overlap = len(common_tokens) / min(len(tokens1), len(tokens2)) if min(len(tokens1), len(tokens2)) > 0 else 0
    return overlap, common_tokens

def filter_narratives(raw_narratives):
    result = {"validNarratives": {}, "excludedNarratives": {}}

    for category, articles in raw_narratives.items():
        print(f"\nProcessing category: {category}")
        if len(articles) < 2:
            result["excludedNarratives"][category] = {"reason": "Less than 2 articles in the narrative."}
            continue

        article_texts = [article["content"] for article in articles]
        similarity = compute_tfidf_similarity(article_texts[0], article_texts[1])
        overlap, common_tokens = compute_keyword_overlap(article_texts[0], article_texts[1])
        print(f"TF-IDF similarity for {category}: {similarity:.2f}")
        print(f"Keyword overlap for {category}: {overlap:.2f}, Common tokens: {list(common_tokens)[:10]}")

        if similarity < 0.1:  # Lowered threshold to 0.1
            result["excludedNarratives"][category] = {
                "reason": f"Articles do not share the same general subject (TF-IDF similarity: {similarity:.2f}, Keyword overlap: {overlap:.2f}).",
                "common_tokens": list(common_tokens)[:10]
            }
            continue

        result["validNarratives"][category] = {"articles": articles}

    return result

# Load raw narratives
with open('raw_narratives.json', 'r') as f:
    raw_narratives = json.load(f)

# Filter narratives
filtered_result = filter_narratives(raw_narratives)

# Save filtered narratives
with open('filtered_narratives.json', 'w') as f:
    json.dump(filtered_result, f, indent=4)

print("Filtered narratives saved to filtered_narratives.json")