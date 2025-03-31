import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pickle
import numpy as np

# Load paths
model_path = "bert_keywords.pth"
tokenizer_path = "tokenizer"
mlb_path = "mlb.pkl"

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

# Load MultiLabelBinarizer
with open(mlb_path, "rb") as f:
    mlb = pickle.load(f)

num_labels = len(mlb.classes_)  # Ensure the model has the correct number of output labels

# Load model with correct num_labels
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=num_labels)
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

def predict_keywords(text, model, tokenizer, mlb, min_threshold=0.3, max_keywords=5):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.sigmoid(outputs.logits).squeeze().cpu().numpy()

    # Set a dynamic threshold based on top-k approach
    sorted_indices = np.argsort(probabilities)[::-1]  # Sort from highest to lowest
    sorted_probs = probabilities[sorted_indices]

    # Apply minimum threshold, but ensure at least `max_keywords` are selected
    selected_indices = sorted_indices[(sorted_probs > min_threshold)][:max_keywords]

    predicted_keywords = [mlb.classes_[i] for i in selected_indices]

    return predicted_keywords


# Test with a sample input
sample_text = "Machine Learning Engineer"
predicted_keywords = predict_keywords(sample_text, model, tokenizer, mlb)
print("Predicted Keywords:", predicted_keywords)