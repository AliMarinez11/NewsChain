import json
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import gensim
from gensim import corpora

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

def perform_topic_modeling(articles):
    processed_articles = [preprocess_text(article).split() for article in articles]
    dictionary = corpora.Dictionary(processed_articles)
    corpus = [dictionary.doc2bow(text) for text in processed_articles]
    
    # Run LDA with adjusted parameters
    lda_model = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=30)
    topics = [lda_model[doc] for doc in corpus]
    
    # Convert topic distributions to vectors
    num_topics = 5
    topic_vector_1 = np.zeros(num_topics)
    topic_vector_2 = np.zeros(num_topics)
    
    for topic_id, prob in topics[0]:
        topic_vector_1[topic_id] = prob
    for topic_id, prob in topics[1]:
        topic_vector_2[topic_id] = prob
    
    # Compute cosine similarity between topic distributions
    topic_similarity = cosine_similarity([topic_vector_1], [topic_vector_2])[0][0]
    print(f"Topic similarity: {topic_similarity:.2f}")  # Debug log
    return topic_similarity > 0.1  # Lowered threshold

def filter_narratives(raw_narratives):
    result = {"validNarratives": {}, "excludedNarratives": {}}

    for category, articles in raw_narratives.items():
        print(f"\nProcessing category: {category}")
        if len(articles) < 2:
            result["excludedNarratives"][category] = {"reason": "Less than 2 articles in the narrative."}
            continue

        article_texts = [article["content"] for article in articles]
        similarity = compute_tfidf_similarity(article_texts[0], article_texts[1])
        print(f"TF-IDF similarity for {category}: {similarity:.2f}")  # Debug log
        if similarity < 0.1:
            result["excludedNarratives"][category] = {"reason": f"Articles do not share the same general subject (TF-IDF similarity: {similarity:.2f})."}
            continue

        # Reintroduce topic modeling check
        if not perform_topic_modeling(article_texts):
            result["excludedNarratives"][category] = {"reason": "Articles do not share a similar dominant topic based on LDA topic modeling."}
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