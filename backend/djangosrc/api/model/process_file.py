from Text_extracn.parsing import extract_text_from_pdf
from llm_insights.mistral import analyze_resume
from Classf_Resume.testing_clasf import predict_job_role
from Return_keywords.Kb_trial import predict_keywords
import os

rel_path = os.path.dirname(os.path.abspath(__file__))
pdf_file_path = rel_path + "/Resume3rd.pdf"
extracted_text = extract_text_from_pdf(pdf_file_path)
print("\n\n\n\nExtracted Text: ",extracted_text, "\n")

analyse_result = analyze_resume(extracted_text)
print("Analyzed Result: ",analyse_result, "\n")

predicted_role = predict_job_role(extracted_text)
predicted_role = predicted_role.strip()
print("Predicted Job Role: ", predicted_role, "\n")

predicted_keywords = predict_keywords(text="Machine Learning Engineer")
print("Predicted Keywords: ", predicted_keywords, "\n\n\n")
