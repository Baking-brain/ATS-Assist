import torch
import pickle
from transformers import BertTokenizer, BertForSequenceClassification

# Load model
model_path = "job_role_classifier.pth"
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=25)  # Change num_labels as per your dataset
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

# Load label encoder
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Function to predict job role
def predict_job_role(resume_text):
    inputs = tokenizer(resume_text, truncation=True, padding=True, max_length=512, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    predicted_label = torch.argmax(outputs.logits, dim=1).item()
    predicted_job_role = label_encoder.inverse_transform([predicted_label])[0]
    return predicted_job_role

# Test with a sample resume
resume_text = """
GAURI SASIKUMAR IYER
504, A-Wing, New Heera Panna CHSShanti Park, Mira Road (E)Thane, Maharashtra– 401107
INDIA  Mobile : 98205 40352  email: gaurisasikumar04@gmail.com
OBJECTIVE
Be a partner in the decision making process by helping the senior management take the right decisions by
extracting insights and identifying patterns from volumes of data collected from various touchpoints of a customer
journey and other key and strategic operations using my skills in data science and analytics.
ACADEMIC BACKGROUND
 Pursuing Bachelors in Computer Science & Engineering (Data Science) from A. P. Shah Institute of
Technology, Thane (2023-2026)
 Higher Secondary Certificate Examination, Maharashtra State Board of Secondary and Higher Secondary
Education, February 2022, T. P. Bhatia Junior College Of Science, Mumbai, Percentage 60
 Secondary School Certificate Examination, Maharashtra State Board of Secondary and Higher Secondary
Education, March 2020, St Xaviers High School, Mumbai, Percentage 80
PROJECTS
 Orderflow: Efficient Restaurant Ordering/Invoicing (Sem 4)
● Developed a Python based restaurant managing application using MySQL and WebSockets devised to
streamline the operations in any restaurant businesses.
● Executed numerous features as Order Log, Automatic bill-generation, Live order tracking, Classified
Menu etc.
● Enabled live order feed to display on chef’s screen using Socketing.
 Intelligent Career Recommender (Sem 3)
● Worked on a Java-based project whose objective is to suggest accurate careers to confused students
using a test based algorithm.
● The application is based on three tests namely Interests, Aptitude and one Subject-based (questions on
Science, Math, Economics etc) and the application gives a suggestion based on the performances of each
test.
● Took use of Java-swing for frontend and used Mysql for an organized backend.
PROFESSIONAL TRAINING / EXPOSURE
● PCAP: Programming Essentials in Python (Cisco Networking Academy)
● Database Foundations (Oracle Academy)
AICTE Eduskills Virtual Internships:
1. Cohort 5 : Network Security Virtual Internship By Fortinet (May-July 2023)
2. Cohort 6 : Data Analytics Process Automation Virtual Internship by Alteryx (Sep-Nov 2023)
3. Cohort 7 : Embedded System Developer Virtual Internship by Microchip (Jan-Mar 2024)
4. Cohort 8 : Juniper Networking Internship (May-June 2024)
5. Cohort 9 : Google Cloud Generative-AI Virtual Internship (July-August 2024)
STRENGTHS
 Strategic: Ability to sort through clutter and make decisions, clear focus and clarity of purpose, a strategic
orientation to data science and high quality implementation. A unique blend of domain expertise
combined with communication knowledge and complementary skill sets
 Learner: Love to learn and grow in a challenging work environment
 Creative: Skilled in creating visually appealing and impactful designs, blending my aesthetic sensibilities
with practical functionality. Adapt creative approaches based on project requirements, ensuring
relevance and resonance with the target audience.Thrive in working with cross-functional teams to
brainstorm and develop creative strategies, fostering a culture of creativity and innovation.Proficient in
crafting compelling narratives that engage and inspire, utilizing a mix of media and formats to convey
messages powerfully.
PERSONAL
I was born on 24th December of the year 2004. My father is a management consultant and my mother is a home
maker. I have an elder brother Vivek Sasikumar Iyer who is a B Tech graduate from SRM University and works as a
Manager at eClerx.
"""
predicted_role = predict_job_role(resume_text)
print("Predicted Job Role:", predicted_role)


'''
CHRONOLOGICAL (INTERNSHIP)
IM A. SAMPLE II 4321 South 55 Street
Bellevue, Nebraska 68005
(402) 291-5432
imasample2@xxx.com
OBJECTIVE: Internship or Part-time Position in Marketing, Public Relations or related
field utilizing strong academic background and excellent communication skills
EDUCATION: BS in Business Administration with Marketing Emphasis
Bellevue University, Bellevue, NE
 Expected Graduation Date: June, 20xx
 GPA to date: 3.56/4.00
Relevant Coursework
Principles of Marketing Business Communication
Internet Marketing Consumer Behavior
Public Relations Business Policy & Stretegy
WORK
HISTORY: Aacademic Tutor (20xx to present)
Bellevue University, Bellevue, NE
 Assist college students in overcoming deficiencies and
successfully mastering academic coursework.
Senior Accounts Receivable Clerk (20xx-20xx)
Lincoln Financial Group, Omaha, NE
 Researched story ideas, wrote articles and participated in the
publication of a weekly in-house newsletter.
 Assisted customers and staff members in resolving problems and
balancing accounts; trained new staff members.
 Managed and recorded daily accounts receivable deposits of up to
$450,000.
 Conducted extensive research to recover lost checks and organized
system to stop payment and replace all checks.
COMMUNITY
SERVICE: Advertising Coordinator, The Vue (20xx to present)
Bellevue University Student Newspaper
Volunteer, Publicity Committee (20xx, 20xx)
Brushup Nebraska Paint-A-Thon
ADDED VALUE: Language Skills: Bilingual (English/Spanish)
Computer Skills: MS Office (Word, Excel, PowerPoint), PhotoShop
REFERENCES: Available Upon Request'''