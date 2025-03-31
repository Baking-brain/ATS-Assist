import pandas as pd
import torch, os
import numpy as np
import pickle
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.preprocessing import MultiLabelBinarizer

rel_path = os.path.dirname(os.path.abspath(__file__))

# Load CSV as Knowledge Base
df = pd.read_csv(rel_path + "/final_keyword_dataset.csv")  # Ensure it has 'Job Role' and 'Keywords' columns

# Load MultiLabelBinarizer (MLB)
with open(rel_path + "/mlb.pkl", "rb") as f:
    mlb = pickle.load(f)

# Load Model and Tokenizer
num_labels = len(mlb.classes_)  # Ensure model matches label count
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=num_labels)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Load Trained Weights
model.load_state_dict(torch.load(rel_path + "/bert_keywords.pth", map_location="cpu"))
model.eval()

# 🔹 Function to Predict Keywords
def predict_keywords(text, model=model, tokenizer=tokenizer, df=df, mlb=mlb, threshold=0.3):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits).cpu().numpy()

    predicted_indices = np.where(probs > threshold)[1]

    # 🔹 Fetch keywords from CSV for the same Job Role
    csv_keywords = df[df["Category"].str.lower() == text.lower()]["Keywords"].values
    csv_keywords = set(kw for kws in csv_keywords for kw in kws.split(','))  # Flatten list

    # 🔹 Combine Model & CSV Results
    model_keywords = set(mlb.classes_[predicted_indices]) if predicted_indices.size > 0 else set()
    final_keywords = list(model_keywords | csv_keywords)  # Merge without duplicates

    return final_keywords if final_keywords else ["No strong match"]

# Example Predictions
# print("Predicted Keywords:", predict_keywords("Machine Learning Engineer", model, tokenizer, df, mlb))