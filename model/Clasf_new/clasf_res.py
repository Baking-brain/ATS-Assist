import os
import torch
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from torch.optim import AdamW
import pickle

# 🔹 Step 1: Load the CSV Containing Valid Job Roles
valid_roles_df = pd.read_csv("unique_job_roles.csv")  # Ensure this file has a "Category" column
valid_job_roles = set(valid_roles_df["Category"].str.lower())  # Convert to lowercase for consistency

# 🔹 Step 2: Load and Filter Resume Dataset
df = pd.read_csv("raw_resume_dataset.csv")
df = df[df["Category"].str.lower().isin(valid_job_roles)]  # Keep only valid job roles

# 🔹 Step 3: Encode Job Roles (After Filtering)
label_encoder = LabelEncoder()
df["Category"] = label_encoder.fit_transform(df["Category"])

# Save Label Encoder for Future Decoding
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# 🔹 Step 4: Tokenization & Dataset Preparation
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

class ResumeDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.encodings = tokenizer(texts.tolist(), truncation=True, padding=True, max_length=max_length, return_tensors="pt")
        self.labels = torch.tensor(labels.to_numpy(), dtype=torch.long)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

# 🔹 Step 5: Train-Test Split
X_train, X_val, y_train, y_val = train_test_split(df["Resume"], df["Category"], test_size=0.2, random_state=42)

train_dataset = ResumeDataset(X_train, y_train, tokenizer)
val_dataset = ResumeDataset(X_val, y_val, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8)

# 🔹 Step 6: Load BERT Model with Correct Label Count
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(label_encoder.classes_))

# Use MPS for Apple M2 or fallback to CPU
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model.to(device)

# Load Checkpoint If Exists
checkpoint_path = "job_role_classifier_latest.pth"
if os.path.exists(checkpoint_path):
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    print("Checkpoint loaded.")

optimizer = AdamW(model.parameters(), lr=2e-5)

# 🔹 Step 7: Training Loop
for epoch in range(3):
    model.train()
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        inputs = {key: val.to(device) for key, val in batch.items()}
        outputs = model(**inputs)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")
    
    # Save Progress
    torch.save(model.state_dict(), checkpoint_path)
    print(f"Checkpoint saved at epoch {epoch+1}")

# 🔹 Step 8: Save Final Model & Label Encoder
torch.save(model.state_dict(), "job_role_classifier.pth")

print("Model (.pth) and label encoder (.pkl) saved successfully.")