from tf_idf import get_tf_idf

skills = ["html", "css", "javascript", "java", "c", "cpp", "python"]

user_skills = ["javascript", "java", "c", "cpp"]

job1 = ["css", "javascript", "cpp", "html"]
job2 = ["java", "cpp", "css"]
job3 = ["java", "css", "python"]
job4 = ["javascript", "c"]
jobs = [
    job1,
    job2,
    job3,
    job4,
]

similarity_scores = (get_tf_idf(all_skills=skills, jobs=jobs, user_skills=user_skills))
print(similarity_scores)

sorted_jobs = dict(sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True))
print(sorted_jobs)