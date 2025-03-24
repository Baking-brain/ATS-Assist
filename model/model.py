import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

# How It Works in Inference (predict_keywords)
# 	1.	The job role text (e.g., "Data Science") is tokenized using BertTokenizer.
# 	2.	The tokenized input is passed to the trained BERT model.
# 	3.	The model outputs logits, which are converted to probabilities using torch.sigmoid().
# 	4.	A threshold (default 0.5) is applied to decide which keywords are predicted.
# 	5.	The decoded keywords (original words) are returned.

class KeywordDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item

    def __len__(self):
        return len(self.labels)

def train_keyword_model(data_path, num_epochs=5):
    # 1. Load and preprocess data
    df = pd.read_csv(data_path)
    
    print("Starting training with:")
    print(f"Original samples: {len(df)}")
    
    # Handle missing values more carefully
    df['Keywords'] = df['Keywords'].fillna('unknown')  # Use 'unknown' instead of empty string
    
    # Convert string keywords to list and clean them, keeping more data
    df['Keywords'] = df['Keywords'].astype(str).apply(
        lambda x: [k.strip() for k in x.split(',') if k.strip() and k.strip().lower() != 'unknown']
        if ',' in x
        else [x.strip()]  # If no comma, treat entire string as one keyword
    )
    
    print(f"\nAfter cleaning, number of samples: {len(df)}")
    print("\nSample of processed keywords:")
    print(df['Keywords'].head())
    print("\nUnique categories:", len(df['Category'].unique()))
    print("Unique keywords:", len(set([k for kw_list in df['Keywords'] for k in kw_list])))
    
    # Create multi-label encoding
    mlb = MultiLabelBinarizer()
    keyword_encodings = mlb.fit_transform(df['Keywords'])
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        df['Category'].values, 
        keyword_encodings,
        test_size=0.2,
        random_state=42
    )
    
    # Initialize BERT
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained(
        'bert-base-uncased',
        num_labels=len(mlb.classes_),
        problem_type="multi_label_classification"
    )
    
    # Create datasets
    train_dataset = KeywordDataset(X_train.tolist(), y_train, tokenizer)
    val_dataset = KeywordDataset(X_val.tolist(), y_val, tokenizer)
    
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8)
    
    # Training setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    
    # Training loop
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        
        for batch in train_loader:
            optimizer.zero_grad()
            
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            total_loss += loss.item()
            
            loss.backward()
            optimizer.step()
        
        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {avg_loss:.4f}")
        
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                val_loss += outputs.loss.item()
        
        print(f"Validation Loss: {val_loss/len(val_loader):.4f}")
    
    return model, tokenizer, mlb

def predict_keywords(text, model, tokenizer, mlb, threshold=0.5):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.sigmoid(outputs.logits)
    
    # Get keywords above threshold
    predicted_labels = (predictions > threshold).squeeze().cpu().numpy()
    predicted_keywords = mlb.inverse_transform(predicted_labels.reshape(1, -1))[0]
    
    return list(predicted_keywords)

if __name__ == "__main__":
    data_path = "../resume_processing_project/data/final_resume_dataset.csv"
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Could not find the dataset at {data_path}")
        
    print(f"Loading data from: {data_path}")
    
    # Train the model
    model, tokenizer, mlb = train_keyword_model(data_path)
    
    # Test with a sample job role
    sample_job = "Data Science"  # Changed to match your categories
    predicted_keywords = predict_keywords(sample_job, model, tokenizer, mlb)
    print(f"Predicted keywords for {sample_job}:")
    print(predicted_keywords)