import requests
from bs4 import BeautifulSoup
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Function to clean boilerplate text
def clean_boilerplate(text):
    # Remove common boilerplate phrases
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
    # Remove extra whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

# Function to compute TF-IDF similarity between two articles
def compute_tfidf_similarity(article1, article2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([article1, article2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity

# Simulated scraper function (replace with your actual scraping logic)
def scrape_articles(search_terms):
    # Placeholder: This should be replaced with your actual scraping logic
    # For now, we'll use the existing narratives_raw.json data as a base
    with open('raw_narratives.json', 'r') as f:
        raw_narratives = json.load(f)
    return raw_narratives

# Main function to scrape and group articles into narratives
def main():
    # Example search terms (replace with your actual search terms)
    search_terms = [
        "Musk Pentagon", "Ukraine Putin", "Department Education", "Boasberg Judge",
        "Canada State", "Biden Former", "King Files", "Government Federal",
        "Democrats Town", "Tesla Musk", "Administration Power", "State Rubio",
        "Walz 2024", "Crisis Been", "First Term", "Maher Food"
    ]

    # Scrape articles (replace with your actual scraping logic)
    raw_narratives = scrape_articles(search_terms)

    # Process narratives to improve quality
    filtered_narratives = {}
    for category, articles in raw_narratives.items():
        if len(articles) < 2:
            continue  # Skip narratives with fewer than 2 articles

        # Clean boilerplate from article content
        cleaned_articles = []
        for article in articles:
            cleaned_content = clean_boilerplate(article['content'])
            # Count words in cleaned content
            word_count = len(cleaned_content.split())
            if word_count < 100:
                continue  # Skip articles with fewer than 100 words
            article['content'] = cleaned_content
            cleaned_articles.append(article)

        if len(cleaned_articles) < 2:
            continue  # Skip narratives with fewer than 2 articles after cleaning

        # Compute TF-IDF similarity between the articles
        similarity = compute_tfidf_similarity(cleaned_articles[0]['content'], cleaned_articles[1]['content'])
        if similarity < 0.2:
            continue  # Skip narratives with TF-IDF similarity below 0.2

        # If the narrative passes all checks, add it to the filtered set
        filtered_narratives[category] = cleaned_articles

    # Save the filtered narratives to raw_narratives.json
    with open('raw_narratives.json', 'w') as f:
        json.dump(filtered_narratives, f, indent=4)

    print(f"Collected {len(filtered_narratives)} narratives, saved to raw_narratives.json")

if __name__ == "__main__":
    main()