import spacy
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load SpaCy NLP Model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Define stopwords and punctuation
stop_words = nlp.Defaults.stop_words
punctuation = set(string.punctuation)

def preprocess_text(text):
    """Lowercase, remove punctuation & stopwords, and tokenize using spaCy"""
    doc = nlp(text.lower())
    words = [token.text for token in doc if token.text not in stop_words and token.text not in punctuation]
    return words

def extract_keywords(text, top_n=20):
    """Extract relevant keywords using TF-IDF, POS filtering, and NER"""
    
    # Step 1: Preprocess text using SpaCy tokenizer
    words = preprocess_text(text)
    
    # Step 2: POS Tagging - Keep only Nouns, Verbs, and Adjectives
    doc = nlp(" ".join(words))
    filtered_words = [token.text for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ"]]

    # Step 3: Named Entity Recognition (NER) - Extract Important Entities
    important_entities = {ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE", "WORK_OF_ART", "LANGUAGE"]}

    # Step 4: TF-IDF Scoring
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(filtered_words)])  # Convert text to vector
    tfidf_scores = dict(zip(vectorizer.get_feature_names_out(), np.ravel(tfidf_matrix.toarray())))

    # Step 5: Keep Top-N Keywords (based on TF-IDF + NER)
    keyword_candidates = set(tfidf_scores.keys()).union(important_entities)
    ranked_keywords = sorted(keyword_candidates, key=lambda x: tfidf_scores.get(x, 0), reverse=True)

    return ranked_keywords[:top_n]  # Return only top-N keywords

# Example Usage
resume_text = """Abhimanyu P Deshmukh
abhimanyudeshmukh34@apsit.edu.in | 8237040509 | Github | Linkedin
EDUCATION
University of Mumbai (GPA: 8/10) Mumbai, India
BE in Computer Science and Engineering- Data Science July 2022- July 2026
●
Courses: Data Structures, Analysis of Algorithm, Statistics for Data Science, Data Mining, Machine Learning, Deep
Learning, Artificial Intelligence, Operating System, Big Data, Computer Networks, Web Computing
SKILLS
Programming Languages: Python, R, Javascript, Java, C, C++
Technology Stack: ETL processing, Tensorflow, Scikit learn, Numpy, Pandas, SQL, PyTorch, Selenium, Beautifulsoup, Git.
(Statistics, Maths, Critical Thinking, Problem Solving)
PROJECTS
●
ATS Assist: Resume Enhancer using NLP and LLMs- Developed a system for improving resumes on aspects like
Grammar, use of keywords and impactful sentence formation using Languagetool API, NLP (BERT with TF-IDF scoring
for relevant keywords) and LLM for sentence generation. TF-IDF will help in scoring the keywords associated with the
job role on which BERT model will be trained on. LLM (mistral) used for text generation catering to specific resumes.
●
VocabLearn: English Vocabulary Enhancer using Leitner approach- Solved challenges of vocabulary improvement
by implementing a flashcard approach (Leitner system) and dynamic difficulty shifting of words using Linear
Regression. Created my own dataset of 1300+ GRE words by performing web scraping using BeautifulSoup (BS4) and
Selenium with the help of Chrome Webdriver from a trusted source. It also showed stats based on users progress.
●
Email Client with user authentication (Developing)- Implementing an email client using IMAP and SMTP protocols
and Django for a smooth backend. GraphQL for API communication and Google OAuth for Security. This project helps
me get a better understanding of communications from APIs and frontend.
●
Property Price Prediction- Created a price prediction model with a dataset for the properties in Bangalore. Performed
ETL (cleaning, Transformation, Outlier Detection). Trained the model on multiple parameters after performing feature
engineering and dimensionality reduction. Tried models like Multi-linear Regression, Lasso Regression.
OPPORTUNITIES
●
Took sessions for students in college on topics like ETL processes (Hands on), use of Tech Stacks (Python) etc through
college clubs and Hacktoberfest.
●
Member of IEEE APSIT student branch in the design team as a co-lead. V olunteered for organising Hacktoberfest in
college campus. (7 days of events, hand on sessions, expert talks)
●
Member of Data Science and Analytics club APSIT. Worked for managing events, ensuring technical facilities and
V olunteering.
ACHIEVEMENTS/ACTIVITIES
●
Hackwave- Participated in a 24hr National level Hackathon. Qualified for 2 rounds of 3. Worked on various machine
learning models and applied ETL concepts to given datasets aiming to create an accurate prediction model. (April 2024)
●
Participated in a 24hr Hackathon at VCET, Vasai in the Cybersecurity domain: Enhancing the security of any given
application using Encryption, Multi-factor Authentication etc. (Oct 2024)
●
2nd place in Matrix of Deception: Inter-departmental Hackathon organized by Data Science and analytics club.
Non-Technical achievements:
● Attended a district level camp for disaster management being a NSS V olunteer for more than a year
● 2nd place in the Badminton tournament at the Ojus sports fest.
CERTIFICATIONS
● PCAP: Programming Essentials in Python (Cisco Networking Academy)
● Database Foundations (Oracle Academy)
AICTE Eduskills Virtual Internships:
1. Cohort 5 : Network Security Virtual Internship By Fortinet (May-July 2023)
2. Cohort 6 : Data Analytics Process Automation Virtual Internship by Alteryx (Sep-Nov 2023)
3. Cohort 7 : Embedded System Developer Virtual Internship by Microchip (Jan-Mar 2024)
4. Cohort 8 : Juniper Networking Internship (May-June 2024)
5. Cohort 9 : Google Cloud Generative-AI Virtual Internship (July-September 2024)
6. Cohort 10: Google for Developers AI-ML Virtual Internship (October-December 2024)"""
keywords = extract_keywords(resume_text, top_n=15)
print("🔹 Extracted Keywords:", keywords)
