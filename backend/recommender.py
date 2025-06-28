import json
import re
import nltk
import os
nltk.data.path.append(os.path.join(os.getcwd(), 'nltk_data'))
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# One-time setup (only run once locally)
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')

def recommend_text(query):
    # Load product catalog
    with open("catalog.json") as f:
        catalog = json.load(f)

    # Initialize
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # Preprocess the query
    query_tokens = nltk.word_tokenize(query.lower())
    query_keywords = [
        lemmatizer.lemmatize(token)
        for token in query_tokens
        if token.isalpha() and token not in stop_words
    ]

    results = []

    for item in catalog:
        # Combine all searchable text fields (add more fields if needed)
        fields = f"{item.get('name', '')} {item.get('description', '')} {' '.join(item.get('tags', []))}".lower()
        fields = re.sub(r"[^\w\s]", "", fields)
        field_tokens = nltk.word_tokenize(fields)
        field_lemmas = [lemmatizer.lemmatize(token) for token in field_tokens if token.isalpha()]

        # Check if any lemmatized keyword is present in lemmatized fields
        if any(keyword in field_lemmas for keyword in query_keywords):
            results.append(item)

    return results[:5]