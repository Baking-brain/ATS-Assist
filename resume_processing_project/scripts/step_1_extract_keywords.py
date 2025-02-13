import pandas as pd
import os
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# Load NLP model
nlp = spacy.load("en_core_web_sm")  # Load small English NLP model

# Load dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/raw_resume_dataset.csv')
df = pd.read_csv(DATA_PATH)

# Sample list of tech-related keywords (can be expanded)
TECH_KEYWORDS = set([
    "Python", "Java", "C++", "JavaScript", "SQL", "Machine Learning", "Deep Learning", "Cloud", "AWS", "Azure",
    "Docker", "Kubernetes", "TensorFlow", "PyTorch", "React", "Node.js", "Linux", "Cybersecurity", "Big Data"
])

# Function to clean and extract keywords
def extract_keywords(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters

    # NLP processing
    doc = nlp(text)

    # Extract nouns, proper nouns, and important words
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ", "VERB"] and not token.is_stop]

    # Keep only meaningful technical keywords
    extracted_keywords = set(keywords) & TECH_KEYWORDS
    return ", ".join(extracted_keywords)

# Apply function
df['Keywords'] = df['Resume'].apply(extract_keywords)

# **TF-IDF for additional keyword extraction**
vectorizer = TfidfVectorizer(max_features=100)  # Extract top 100 keywords
tfidf_matrix = vectorizer.fit_transform(df['Resume'].fillna(""))

# Add top TF-IDF words to keywords
feature_names = vectorizer.get_feature_names_out()
for i in range(len(df)):
    top_tfidf_words = [feature_names[j] for j in tfidf_matrix[i].toarray().argsort()[0][-5:]]  # Get top 5
    df.at[i, 'Keywords'] += ", " + ", ".join(top_tfidf_words)

# Save cleaned dataset
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '../data/cleaned_resume_dataset.csv')
df[['Job Role', 'Keywords']].to_csv(OUTPUT_PATH, index=False)

print(f"Advanced keyword extraction complete! Saved to {OUTPUT_PATH}")
