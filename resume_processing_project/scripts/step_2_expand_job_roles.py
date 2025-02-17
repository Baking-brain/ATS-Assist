import pandas as pd
import random

# Load cleaned dataset
input_file = "../data/cleaned_resume_dataset.csv"
df = pd.read_csv(input_file)

# Define additional job roles and relevant skills
new_roles = {
    "AI Engineer": "Machine Learning, Deep Learning, TensorFlow, PyTorch, NLP, Computer Vision",
    "HR Coordinator": "Recruitment, Onboarding, Payroll Processing, Employee Relations, Benefits Administration",
    "Cloud Engineer": "AWS, Azure, Kubernetes, Docker, DevOps, Terraform",
    "Data Analyst": "SQL, Tableau, Power BI, Data Visualization, Python, Excel",
    "Cybersecurity Analyst": "Network Security, Ethical Hacking, SIEM, Firewalls, Threat Intelligence",
    "Blockchain Developer": "Smart Contracts, Solidity, Ethereum, Cryptography, Hyperledger",
    "Payroll Specialist": "Payroll Processing, Tax Compliance, Accounting Software, Time Tracking"
}

# Generate multiple variations per job role
expanded_roles = []
for role, skills in new_roles.items():
    skill_list = skills.split(", ")
    for _ in range(10):  # Create 10 variations per role
        varied_skills = random.sample(skill_list, k=random.randint(4, len(skill_list)))
        expanded_roles.append([role, ", ".join(varied_skills)])

# Convert to DataFrame
df_expanded = pd.DataFrame(expanded_roles, columns=["Category", "Keywords"])

# Merge with existing data
df_final = pd.concat([df, df_expanded], ignore_index=True)

# Save expanded dataset
output_file = "../data/expanded_resume_dataset.csv"
df_final.to_csv(output_file, index=False)

print(f"Job roles expanded and saved to {output_file}")
