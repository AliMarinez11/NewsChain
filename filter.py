import json
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def filter_narratives(raw_narratives):
    result = {"validNarratives": {}, "excludedNarratives": {}}

    for category, articles in raw_narratives.items():
        print(f"\nProcessing category: {category}")
        if len(articles) < 2:
            result["excludedNarratives"][category] = {"reason": "Less than 2 articles in the narrative."}
            continue

        article_texts = [article["content"] for article in articles]
        similarity = compute_tfidf_similarity(article_texts[0], article_texts[1])
        print(f"TF-IDF similarity for {category}: {similarity:.2f}")
        if similarity < 0.15:  # Increased threshold to 0.15
            result["excludedNarratives"][category] = {"reason": f"Articles do not share the same general subject (TF-IDF similarity: {similarity:.2f})."}
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