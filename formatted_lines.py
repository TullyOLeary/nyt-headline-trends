import os
from dotenv import load_dotenv
import requests
from collections import Counter
from nltk.corpus import stopwords
from concurrent.futures import ThreadPoolExecutor
import spacy

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('API_KEY')
# Load the spaCy language model
nlp = spacy.load('en_core_web_sm')  # Use spaCy for efficient NLP processing


def fetch_articles(api_key, period):
    url = f"https://api.nytimes.com/svc/mostpopular/v2/viewed/{period}.json"
    params = {"api-key": api_key}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def process_articles(articles):
    combined_text = []
    seen_articles = set()

    for article in articles:
        article_url = article.get('url')
        if article_url not in seen_articles:
            seen_articles.add(article_url)
            title = article.get('title', "")
            abstract = article.get('abstract', "")
            combined_text.append(f"{title} {abstract}")

    return " ".join(combined_text).lower()


def clean_and_filter_text(text):
    # Tokenization and stopword removal using spaCy
    doc = nlp(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [
        token.text for token in doc
        if token.is_alpha and token.text not in stop_words
    ]
    return filtered_words


def get_and_format_lines(api_key):
    periods = [1, 7, 30]

    # Fetch articles concurrently
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda period: fetch_articles(api_key, period), periods))

    # Combine and process all articles
    combined_articles = [article for result in results for article in result]
    full_text = process_articles(combined_articles)

    # Clean and filter text
    filtered_words = clean_and_filter_text(full_text)

    # Get the top 66 most common words
    word_counts = [word for word, count in Counter(filtered_words).most_common(66)]

    # Format and capitalize the words into the desired lines
    line_lengths = list(range(1, 12))
    current_index = 0
    formatted_lines = []

    for line_length in line_lengths:
        line = " ".join(word_counts[current_index:current_index + line_length])
        current_index += line_length

        # Custom capitalize logic
        capitalized_words = [
            word.upper() if len(word) == 2 and word.lower() != 'mr' else word.capitalize()
            for word in line.split()
        ]
        formatted_lines.append(' '.join(capitalized_words))

    return formatted_lines

