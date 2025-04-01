import torch
import pickle
import numpy as np
import matplotlib.pyplot as plt
from transformers import BertTokenizer, BertForSequenceClassification

# Load model
model_path = "job_role_classifier.pth"
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=25)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

# Load label encoder
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Function to predict job role probabilities
def predict_job_role_probs(resume_text):
    inputs = tokenizer(resume_text, truncation=True, padding=True, max_length=512, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()[0]  # Convert to probability distribution
    return {label_encoder.inverse_transform([i])[0]: probs[i] for i in range(len(probs))}

# Sample Resume
resume_text = """
Experienced Data Scientist with a strong background in machine learning, deep learning, and AI. 
Skilled in Python, TensorFlow, and cloud computing with AWS. Developed multiple NLP models for business insights.
"""

# Get predictions
job_role_probs = predict_job_role_probs(resume_text)

# Sort top 5 job roles
sorted_roles = sorted(job_role_probs.items(), key=lambda x: x[1], reverse=True)[:5]

# Plot Bar Chart
roles, probabilities = zip(*sorted_roles)
plt.figure(figsize=(10, 5))
plt.barh(roles, probabilities, color="skyblue")
plt.xlabel("Probability Score")
plt.ylabel("Job Role")
plt.title("Top 5 Predicted Job Roles for the Resume")
plt.gca().invert_yaxis()  # Highest probability on top
plt.show()