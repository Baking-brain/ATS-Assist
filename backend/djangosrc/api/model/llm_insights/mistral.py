import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

if not HUGGINGFACE_API_KEY:
    raise ValueError("Missing required API key. Please set HUGGINGFACE_API_KEY in your .env file")

# Initialize Hugging Face client
client = InferenceClient(token=HUGGINGFACE_API_KEY)

# Default evaluation rubric
DEFAULT_RUBRIC = """Please evaluate this resume based on the following criteria:
1. Skills Match (0-10): Alignment of technical and soft skills with job requirements
2. Experience Relevance (0-10): Relevance and depth of past experiences
3. Education Fit (0-10): Educational background's relevance to the role
4. Achievement Impact (0-10): Quantifiable achievements and their significance
5. Overall Presentation (0-10): Resume formatting, clarity, and professionalism

For each criterion:
- Provide a score out of 10
- Give specific feedback
- Suggest improvements

Then calculate:
- Total Score: Sum of all criteria (max 50)
- Match Percentage: Total score as a percentage
- Final Recommendation: Shortlist/Consider/Reject based on match percentage

Format your response as follows:
[Scoring]
- List each criterion score and feedback

[Improvements]
- Specific suggestions for each section

[Final Assessment]
- Total Score: X/50
- Match Percentage: X%
- Recommendation: [Shortlist/Consider/Reject]"""

# Set your resume text here
resume_text = """
Abhimanyu P Deshmukh
abhimanyudeshmukh34@apsit.edu.in | 8237040509 | Github  | Linkedin
EDUCATION
University of Mumbai (GPA: 8/10)                                                                       Mumbai, India
BE in Computer Science and Engineering- Data Science                                            July 2022- July 2026
 ●  Courses: Data Structures, Analysis of Algorithm, Statistics for Data Science, Data Mining, Machine Learning, Deep
    Learning, Artificial Intelligence, Operating System, Big Data, Computer Networks, Web Computing
SKILLS
Programming Languages: Python, R, Javascript, Java, C, C++
Technology Stack: ETL processing, Tensorflow, Scikit learn, Numpy, Pandas, SQL, PyTorch, Selenium, Beautifulsoup, Git.
(Statistics, Maths, Critical Thinking, Problem Solving)
PROJECTS
 ●  ATS Assist: Resume Enhancer using NLP and LLMs- Developed a system for improving resumes on aspects like
    Grammar, use of keywords and impactful sentence formation using Languagetool API, NLP (BERT with TF-IDF scoring
    for relevant keywords) and LLM for sentence generation. TF-IDF will help in scoring the keywords associated with the
    job role on which BERT model will be trained on. LLM (mistral) used for text generation catering to specific resumes.
 ●  VocabLearn: English Vocabulary Enhancer using Leitner approach- Solved challenges of vocabulary improvement
    by  implementing a flashcard approach (Leitner system) and dynamic difficulty shifting of words using Linear
    Regression. Created my own dataset of 1300+ GRE words by performing web scraping using BeautifulSoup (BS4) and
    Selenium with the help of Chrome Webdriver from a trusted source. It also showed stats based on users progress.
 ●  Email Client with user authentication (Developing)- Implementing an email client using IMAP and SMTP protocols
    and Django for a smooth backend. GraphQL for API communication and Google OAuth for Security. This project helps
    me get a better understanding of communications from APIs and frontend.
 ●  Property Price Prediction- Created a price prediction model with a dataset for the properties in Bangalore. Performed
    ETL (cleaning, Transformation, Outlier Detection). Trained the model on multiple parameters after performing feature
    engineering and dimensionality reduction. Tried models like Multi-linear Regression, Lasso Regression.
OPPORTUNITIES
 ●  Took sessions for students in college on topics like ETL processes (Hands on), use of Tech Stacks (Python) etc through
    college clubs and Hacktoberfest.
 ●  Member of IEEE APSIT student branch in the design team as a co-lead. Volunteered for organising Hacktoberfest in
    college campus. (7 days of events, hand on sessions, expert talks)
 ●  Member of Data Science and Analytics club APSIT. Worked for managing events, ensuring technical facilities and
    Volunteering.
ACHIEVEMENTS/ACTIVITIES
 ●  Hackwave- Participated in a 24hr National level Hackathon. Qualified for 2 rounds of 3. Worked on various machine
    learning models and applied ETL concepts to given datasets aiming to create an accurate prediction model. (April 2024)
 ●  Participated in a 24hr Hackathon at VCET, Vasai in the Cybersecurity domain: Enhancing the security of any given
    application using Encryption, Multi-factor Authentication etc. (Oct 2024)
 ●  2nd place in Matrix of Deception: Inter-departmental Hackathon organized by Data Science and analytics club.
Non-Technical achievements:
    ● Attended a district level camp for disaster management being a NSS Volunteer for more than a year
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
    6. Cohort 10: Google for Developers AI-ML Virtual Internship (October-December 2024)
"""

def analyze_resume(resume_text):
    """Analyze a resume text using the Hugging Face API"""
    try:
        messages = [
            {"role": "system", "content": f"You are an ATS system and recruiter. Evaluate the resume using this rubric:\n{DEFAULT_RUBRIC}"},
            {"role": "user", "content": resume_text}
        ]
        
        response = client.chat_completion(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=messages,
            temperature=0.5,
            max_tokens=2048,
            top_p=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Run analysis and print the result
if __name__ == "__main__":
    analysis_result = analyze_resume(resume_text)
    print("\n" + "="*50)
    print("RESUME ANALYSIS RESULT")
    print("="*50)
    print(analysis_result)