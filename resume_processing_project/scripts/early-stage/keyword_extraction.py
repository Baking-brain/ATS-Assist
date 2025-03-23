import re
import spacy
import string
from nltk.corpus import stopwords
import nltk

# Download stopwords (if not already downloaded)
nltk.download("stopwords")
stop_words = set(stopwords.words('english'))

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_md")

def clean_text(text):
    """
    Cleans the input resume text by:
    - Removing URLs, emails, special characters
    - Removing stopwords
    - Keeping only meaningful words
    """
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    
    # Remove emails
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "", text)
    
    # Remove special characters and digits
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove stopwords
    text = " ".join([word for word in text.split() if word not in stop_words])
    
    return text

def extract_keywords(text):
    """
    Extracts important keywords from the cleaned resume using SpaCy
    - Filters out stopwords, punctuations, and common words
    - Returns top keywords based on POS tagging
    """
    doc = nlp(text)
    keywords = []

    for token in doc:
        if (token.is_alpha and token.text not in stop_words and 
            token.pos_ in ["NOUN", "PROPN", "ADJ", "VERB"]):  # Keep meaningful words
            keywords.append(token.text)

    return list(set(keywords))  # Remove duplicates

# Sample Resume (Modify this to test on different resumes)
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

# Step 1: Clean the resume
cleaned_resume = clean_text(resume_text)
print("🔹 Cleaned Resume:\n", cleaned_resume, "\n")

# Step 2: Extract Keywords
keywords = extract_keywords(cleaned_resume)
print("🔹 Extracted Keywords:\n", keywords)