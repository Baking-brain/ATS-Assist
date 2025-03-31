# ATS-Assist: NLP-Based Resume Enhancer
A resume enhancer leveraging NLP and Classification

## Overview
ATS-Assist is an AI-powered resume enhancement tool that analyzes resumes using Natural Language Processing (NLP) and suggests relevant keywords to improve their alignment with industry expectations and Applicant Tracking Systems (ATS). The system extracts text from resumes, classifies job roles, and generates domain-specific keywords to help users refine their resumes for better job matching.

## Tech Stack
- **Programming Language:** Python
- **Machine Learning:** BERT (Bidirectional Encoder Representations from Transformers)
- **Text Extraction:** LLAMA Parse
- **Frameworks & Libraries:**
  - Transformers (Hugging Face)
  - PyTorch
  - Scikit-learn
  - Pandas & NumPy
  - Torchvision & Torchtext
- **Backend:** Django (for API integration)
- **Frontend:** React (for UI)
- **Database:** PostgreSQL (for storing parsed resumes and model outputs)

## Key Features
1. **Resume Parsing & Text Extraction**
   - Extracts structured text from PDF resumes using LLAMA Parse.
2. **Job Role Classification**
   - Classifies resumes into relevant job categories (e.g., Data Scientist, Software Engineer) using a BERT-based classifier.
3. **Keyword Suggestion Model**
   - Suggests domain-specific keywords based on the classified job role using a fine-tuned BERT model.
4. **Resume Optimization**
   - Helps users identify key technologies and skills to add to their resumes.

## Workflow
1. **Resume Upload & Parsing**
   - User uploads a resume (PDF), which is processed through LLAMA Parse to extract text.
2. **Job Role Classification**
   - The extracted text is passed to a pre-trained BERT classifier, which assigns a job role tag.
3. **Keyword Generation**
   - The classified job role is used as input to a BERT-based keyword extraction model.
4. **Result Output**
   - The model suggests relevant keywords that can enhance the resume.

## Installation & Setup
### Prerequisites
- Python 3.8+
- PyTorch
- Transformers (Hugging Face)
- PostgreSQL (for database storage)
- Django & Django REST Framework

### Installation
```sh
# Clone the repository
git clone https://github.com/Baking-brain/ATS-Assist.git
cd ATS-Assist

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Future Enhancements
- Improve classification accuracy with domain-specific embeddings.
- Integrate real-time resume feedback.
- Expand dataset for more precise keyword generation.
- Add multilingual support for non-English resumes.

## Contributing
We welcome contributions! Feel free to submit issues, fork the repo, and create pull requests.

## License
This project is licensed under the Skibidi License.
