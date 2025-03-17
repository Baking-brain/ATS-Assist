import os

print("Running step 1: Extracting Keywords")
os.system("python3 Users/abhimanyudeshmukh/code/projectsem6/ATS-Assist/resume_processing_project/scripts/step_1_extract_keywords.py")

print("Running step 2: Expanding Job Roles")
os.system("python3 Users/abhimanyudeshmukh/code/projectsem6/ATS-Assist/resume_processing_project/scripts/step_2_expand_job_roles.py")

print("Running step 3: Fixing HR Skills")
os.system("python3 Users/abhimanyudeshmukh/code/projectsem6/ATS-Assist/resume_processing_project/scripts/step_3_fix_hr_section.py")

print("All steps completed! Final dataset saved in /data/final_resume_dataset.csv")
