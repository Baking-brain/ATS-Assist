import math
from .cosine_similarity import cos_sim

def get_tf_idf(all_skills, user_skills, jobs):


    #Calculate TF score for user skills
    user_tf_score = {}
    for skill in all_skills:
        if skill in user_skills:
            user_tf_score[skill] = round(1/(len(user_skills)+1), 3)
        else:
            user_tf_score[skill] = 0


    #Calculate TF scores for each job
    jobs_tf_score = []
    for job in jobs:
        temp_job_tf_score = {}
        for skill in all_skills:
            if skill in job:
                temp_job_tf_score[skill] = round(1/(len(job)+1), 3)
            else:
                temp_job_tf_score[skill] = 0
        jobs_tf_score.append(temp_job_tf_score)



    #Calculate IDF score for each skill
    idf_scores = {}
    for skill in all_skills:
        skill_count = 0
        for job in jobs:
            if skill in job:
                skill_count += 1
        idf_scores[skill] = round(math.log((len(jobs)+1)/(skill_count+1)), 3)


    #Calculate user vector
    user_vector = [i*j for i,j in zip(user_tf_score.values(), idf_scores.values())]


    #Calculate job vector for each job
    job_vectors = []
    for job_tf_score in jobs_tf_score:
        job_vector = [i*j for i,j in zip(job_tf_score.values(), idf_scores.values())]
        job_vectors.append(job_vector)


    #Calculate similarity score for each job requirement w.r.t. user skills
    i = 0
    cos_sim_scores = {}
    for job_vector in job_vectors:
        i += 1
        cos_sim_scores[f'job{i}'] = (cos_sim(user_vector, job_vector))





    print(f'\n\nUser TF score: {user_tf_score}\n\nJobs TF scores: {jobs_tf_score}\n\nIDF scores: {idf_scores}\n\n')
    print(f'\n\nUser vector: {user_vector}\n\nJobs vectors: {job_vectors}\n\n')


    return cos_sim_scores
