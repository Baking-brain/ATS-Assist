import pandas as pd

# Load expanded dataset
input_file = "../data/expanded_resume_dataset.csv"
df = pd.read_csv(input_file)

# Define correct HR-related skills
hr_skills = {
    "HR Manager": "Recruitment, Talent Acquisition, Employee Relations, HR Policies, Payroll, Compliance",
    "HR Coordinator": "Onboarding, Benefits Administration, HR Software, Conflict Resolution, Performance Management"
}

# Update HR job roles with correct skills
df["Keywords"] = df.apply(
    lambda row: hr_skills[row["Category"]] if row["Category"] in hr_skills else row["Keywords"], axis=1
)

# Save corrected dataset
output_file = "../data/final_resume_dataset.csv"
df.to_csv(output_file, index=False)

print(f"HR skills corrected and final dataset saved to {output_file}")
