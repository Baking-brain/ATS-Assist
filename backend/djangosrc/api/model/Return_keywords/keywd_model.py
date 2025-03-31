# How It Works in Inference (predict_keywords)
# 	1.	The job role text (e.g., "Data Science") is tokenized using BertTokenizer.
# 	2.	The tokenized input is passed to the trained BERT model.
# 	3.	The model outputs logits, which are converted to probabilities using torch.sigmoid().
# 	4.	A threshold (default 0.5) is applied to decide which keywords are predicted.
# 	5.	The decoded keywords (original words) are returned.
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os
import pickle

class KeywordDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=64):
        self.encodings = tokenizer(
            texts, truncation=True, padding=True, max_length=max_length
        )
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

def train_keyword_model(data_path, num_epochs=5):
    df = pd.read_csv(data_path)
    save_dir = os.path.dirname(data_path)

    print("Starting training with:")
    print(f"Original samples: {len(df)}")

    df["Keywords"] = df["Keywords"].fillna("unknown")
    df["Keywords"] = df["Keywords"].astype(str).apply(
        lambda x: [k.strip() for k in x.split(",") if k.strip() and k.strip().lower() != "unknown"]
    )

    mlb = MultiLabelBinarizer()
    keyword_encodings = mlb.fit_transform(df["Keywords"])

    X_train, X_val, y_train, y_val = train_test_split(
        df["Category"].tolist(), keyword_encodings, test_size=0.2, random_state=42
    )

    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased", num_labels=len(mlb.classes_), problem_type="multi_label_classification"
    )

    train_dataset = KeywordDataset(X_train, y_train, tokenizer)
    val_dataset = KeywordDataset(X_val, y_val, tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8)

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()

            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {total_loss / len(train_loader):.4f}")

    # Save model, tokenizer, and mlb
    model_path = os.path.join(save_dir, "bert_keywords.pth")
    tokenizer_path = os.path.join(save_dir, "tokenizer")
    mlb_path = os.path.join(save_dir, "mlb.pkl")

    torch.save(model.state_dict(), model_path)
    tokenizer.save_pretrained(tokenizer_path)
    with open(mlb_path, "wb") as f:
        pickle.dump(mlb, f)

    print(f"Model saved to {model_path}")
    print(f"Tokenizer saved to {tokenizer_path}")
    print(f"MLB saved to {mlb_path}")

    return model, tokenizer, mlb

def predict_keywords(text, model, tokenizer, mlb, threshold=0.5):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits).cpu().numpy()

    predicted_indices = np.where(probs > threshold)[1]  # Select only confident predictions

    return mlb.classes_[predicted_indices] if predicted_indices.size > 0 else ["No strong match"]

if __name__ == "__main__":
    data_path = "final_keyword_dataset.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Could not find the dataset at {data_path}")

    model, tokenizer, mlb = train_keyword_model(data_path)
    
    test_categories = ["Machine Learning Engineer", "Data Scientist"]
    for category in test_categories:
        predicted_keywords = predict_keywords(category, model, tokenizer, mlb)
        print(f"Predicted keywords for {category}: {predicted_keywords}")


# def predict_keywords(text, model, tokenizer, mlb, threshold=0.5):
#     model.eval()
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
#     device = next(model.parameters()).device
#     inputs = {k: v.to(device) for k, v in inputs.items()}
    
#     with torch.no_grad():
#         outputs = model(**inputs)
#         predictions = torch.sigmoid(outputs.logits)
    
#     # Get keywords above threshold
#     predicted_labels = (predictions > threshold).squeeze().cpu().numpy()
#     predicted_keywords = mlb.inverse_transform(predicted_labels.reshape(1, -1))[0]
    
#     return list(predicted_keywords)