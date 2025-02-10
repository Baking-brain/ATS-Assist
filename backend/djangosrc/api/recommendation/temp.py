from tf_idf import get_tf_idf

skills = ["html", "css", "javascript", "java", "c", "cpp", "python"]

user_skills = ["javascript", "java", "c", "cpp"]

job1 = ["css", "javascript", "cpp", "html"]
job2 = ["java", "python", "css"]
job3 = ["java", "css", "python"]
job4 = ["javascript", "c"]
jobs = [
    job1,
    job2,
    job3,
    job4
]

sim_scores = (get_tf_idf(all_skills=skills, jobs=jobs, user_skills=user_skills))
print(sim_scores)

for score in sorted(list(sim_scores.values()))[::-1]:
    temp = list(sim_scores.keys())[list(sim_scores.values()).index(score)]
    print(temp)