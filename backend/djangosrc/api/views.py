import os
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from .serializers import ApplicantSerializer, SkillSerializer, GetApplicantSkillsSerializer, GetApplicantProfileSerializer, JobSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from .authentication import custom_jwtauthentication
from rest_framework.permissions import IsAuthenticated
from .models import Applicant, Skill, Job
from django.db.models import Prefetch
from rest_framework.parsers import MultiPartParser, FormParser
from .recommendation.cosine_similarity import cos_sim
from .recommendation.recommend_jobs import recommend_similar_jobs
from .model import process_file

# Create your views here.
class test_view(APIView):
    def get(self, request, *kwargs, **args):
        return Response({"Server":"Running"},status=200)
    
class get_applicants(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        applicants = Applicant.objects.all()
        applicants = ApplicantSerializer(applicants, many = True).data

        return Response({"Applicants":applicants})

class create_applicant(APIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_data = request.data

        if not (user_data['username'] and user_data['password']):
            raise Exception("Details missing or not provided")

        applicant = Applicant.objects.create_user(**user_data)

        return Response({"status": "ok"})
    
class login(APIView):
    
    #{"username":"test1","password":"1234"}
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        print(username, password)

        if (not username) or (not password):
            raise exceptions.ValidationError("Credentials not provided")


        try:
            user = Applicant.objects.get(username=username)

            check_password = user.check_password(password)
            if check_password:
                token = RefreshToken.for_user(user)
                response = Response({"Profile":GetApplicantProfileSerializer(user).data})

                response.set_cookie("access_token", str(token.access_token))
                response.set_cookie("refresh_token", str(token))

                return response
            
            else:
                return Response({"status":"Incorrect Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    
        except Exception as e:
            print("\n\nGenerate Error: ",e)
            
            if "Applicant matching query does not exist" in str(e):
                return Response({"status":"Incorrect credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({"status":"Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)

class refresh_token(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        try:
            old_refresh_token = request.COOKIES.get('refresh_token')
            if not old_refresh_token:
                raise InvalidToken()


            new_token = RefreshToken(old_refresh_token)
            
            response = Response({"new access_token":str(new_token.access_token), "refresh_token":str(new_token)})
            response.set_cookie("access_token", new_token.access_token)
            response.set_cookie("refresh_token", new_token)

            return response

        except Exception as e:
            if 'expired' in str(e):
                raise InvalidToken('Refresh token expired')
            else:
                print(f'\n\nError => {e}\n\n')
                return Response({"status":"Something went wrong refresh token"})

class logout(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        if (not request.COOKIES.get('access_token') or (not request.COOKIES.get('refresh_token'))):
            return Response({"status":"no token found"})

        response = Response({"status":"ok"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response

class get_profile(APIView):

    authentication_classes = [custom_jwtauthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        applicant = Applicant.objects.get(username = request.user)
        applicant = GetApplicantProfileSerializer(applicant).data
        applicant['skills'] = [Skill.objects.get(id=skill_id).name for skill_id in applicant['skills']]

        return Response({"Profile":applicant})

class serve_react(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return render(request, 'index.html')
    
class add_skills(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        applicants = Applicant.objects.all()
        applicants = ApplicantSerializer(applicants, many = True).data

        skills = SkillSerializer(Skill.objects.all(), many=True).data

        return Response({"Applicants":applicants, "Skills":skills})

    def post(self, request):

        username = request.data['username']
        user_skills_to_be_added = request.data['skills']

        applicant = Applicant.objects.get(username=username)

        #Get all skill names
        temp_all_skills = SkillSerializer(Skill.objects.all(), many=True).data
        all_skills = []
        for temp_skill in temp_all_skills:
            all_skills.append(temp_skill['name'])

        for skill in user_skills_to_be_added:
            skill = skill.lower().strip()
            if skill not in all_skills:
                Skill.objects.create(name=skill)
                print("Created: ", skill)

            skill_object = Skill.objects.get(name=skill)

            applicant.skills.add(skill_object)
            

        return Response()

class get_similar_applicants(APIView):
    authentication_classes = [custom_jwtauthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        username = request.user

        #Get all existing skill ids
        temp_all_skills = SkillSerializer(Skill.objects.all(), many=True).data
        all_skill_ids = []
        for temp_skill in temp_all_skills:
            all_skill_ids.append(temp_skill['id'])
        all_skill_ids = sorted(all_skill_ids)

        #Get all applicants skill-ids in an object i.e key value pairs
        temp_applicants = GetApplicantSkillsSerializer(Applicant.objects.exclude(username=username), many=True).data
        applicants = {}
        for applicant in temp_applicants:
            applicants[applicant['username']] = applicant['skills']

        #Get user skill ids
        user_skill_ids = ApplicantSerializer(Applicant.objects.get(username=username)).data['skills']

        #Create user vector
        user_vector = []
        for skill_id in all_skill_ids:
            if skill_id in user_skill_ids:
                user_vector.append(1)
            else:
                user_vector.append(0)
        
        #Convert all applicants skill into vectors
        for applicant, indvisual_skills in applicants.items():
            temp_vector = []
            for skill_id in all_skill_ids:
                if skill_id in indvisual_skills:
                    temp_vector.append(1)
                else:
                    temp_vector.append(0)

            similarity_score = cos_sim(user_vector, temp_vector)
            # print(applicant, similarity_score)
            applicants[applicant] = similarity_score
        
        #Sort according to scores in descending order and filter with score 0 (not at all relevant)
        applicants = dict(sorted(
                                (applicant for applicant in applicants.items() if applicant[1] != 0),
                                key=lambda item: item[1], reverse=True
                                 )
                          )
        
        print("\nSorted similar applicants: \n", applicants)
        
        #Get similar applicants profile
        similar_profiles = []
        for applicant in applicants.keys():
            temp_profile = GetApplicantProfileSerializer(Applicant.objects.get(username=applicant)).data

            #Convert skill ids into skill names
            temp_skills = []
            for skill_id in temp_profile['skills']:
                skill = Skill.objects.get(id=skill_id)
                temp_skills.append(skill.name)
            temp_profile['skills'] = temp_skills
            similar_profiles.append(temp_profile)

        return Response({"Applicants":similar_profiles, "Scores":applicants})

class add_jobs(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        jobs = JobSerializer(Job.objects.all(), many=True).data

        return Response({"Jobs":jobs})
    
    """
    {
    "name":"Job1",
    "requirements":["JavaScript", "HTML", "CSS", "Python"]
    }
    """

    def post(self, request):
        job_requirements = request.data['req']

        all_skills = SkillSerializer(Skill.objects.all(), many=True).data
        all_skills = [skill['name'] for skill in all_skills]


        #Format all requirements and check if the skill exists
        job_requirements = [[job2.lower().strip() for job2 in job1] for job1 in job_requirements]

        job_req_id = []
        for ind_job in job_requirements:
            temp_job_id = []
            for job_req in ind_job:
                if job_req not in all_skills:
                    print("\nNot Found\n")
                else:
                    skill = Skill.objects.get(name=job_req)
                    temp_job_id.append(skill.id)
            job_req_id.append(temp_job_id)
        

        jobs = Job.objects.all()
        for job, reqs in zip(jobs, job_req_id):
            print(job, reqs)
            # job.requirements.add(*reqs)

        print(job_req_id)


    
        return Response({"Jobs Req":job_requirements})

class get_similar_jobs(APIView):
    authentication_classes = [custom_jwtauthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        username = request.user

        #Get user skills names
        user = Applicant.objects.get(username=username)
        user_skills = [skill.name for skill in user.skills.all()]


        #Get all skill names
        all_skills = [skill.name for skill in Skill.objects.all()]

        jobs = Job.objects.all()

        all_jobs_requirements = []
        for job in jobs:
            job_req = [req.name for req in job.requirements.all()]
            all_jobs_requirements.append(job_req)

        generic_recommended_jobs = recommend_similar_jobs(all_skills=all_skills, user_skills=user_skills, all_jobs_requirements=all_jobs_requirements)

        recommended_jobs = [] 
        for job_name_index, score in generic_recommended_jobs.items():
            if not score:
                continue
            temp_job = jobs[int(job_name_index[-1]) - 1]
            temp_job = JobSerializer(temp_job).data
            temp_job['requirements'] = [Skill.objects.get(id=skill_id).name for skill_id in temp_job['requirements']]
            recommended_jobs.append(temp_job)



        return Response({"Jobs":recommended_jobs})

class get_search_results(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        #Get parameters from query
        search_type = request.GET.get('search_type', None)
        search_string = request.GET.get('search_string', None)
        search_string = search_string.strip().lower()

        #Check if search type is provided
        if not search_type:
            raise SyntaxError("Search type not provided")
        
        #Check if search string is provided
        if not search_string:
            return Response([])

        #Return search query results for applicants
        if search_type == 'applicants':
            # Filter skills by search string
            matching_skills = Skill.objects.filter(name__icontains=search_string)
            
            # Get applicants with skills that match the search
            applicants = Applicant.objects.filter(skills__in=matching_skills).distinct()

            # Prefetch skills associated with the applicants to avoid multiple queries
            applicants = applicants.prefetch_related('skills')

            # Prepare the data for response
            applicant_data = []
            for applicant in applicants:
                # Extract skills associated with the applicant
                temp_skills = [skill.name for skill in applicant.skills.all()]
                print(applicant.skills.all())

                # Prepare the applicant info with skills
                applicant_info = GetApplicantProfileSerializer(applicant).data

                #Convert skill ids into skill names
                temp_skills = []
                for skill_id in applicant_info['skills']:
                    skill = Skill.objects.get(id=skill_id)
                    temp_skills.append(skill.name)
                applicant_info['skills'] = temp_skills

                applicant_data.append(applicant_info)

            # Return the unique list of applicants (distinct already handled by query)
            return Response(applicant_data)
        

        #Return search query results for jobs
        # elif search_type == 'jobs' :

        #     jobs = []
        #     matching_skills = Skill.objects.filter(name__icontains=search_string)
        #     for skill in matching_skills:
        #         temp_jobs = JobSerializer(skill.jobs.all(), many=True).data
        #         for temp_job in temp_jobs:

        #             temp_skills_index = temp_job['requirements']
        #             temp_skills = []
        #             for skill_index in temp_skills_index:
        #                 temp_skill_name = Skill.objects.get(id=skill_index).name
        #                 temp_skills.append(temp_skill_name)

        #             temp_job = {'username': temp_job['company'],'skills':temp_skills}
        #             jobs.append(temp_job)



        #     #Filter applicants to remove duplicates
        #     seen_jobs = set()
        #     filtered_jobs = []
        #     for job in jobs:
        #         if job['username'] not in seen_jobs:
        #             filtered_jobs.append(job)
        #             seen_jobs.add(job['username'])

        #     return Response(filtered_jobs)

        elif search_type == 'jobs':

            # Filter skills by search string
            matching_skills = Skill.objects.filter(name__icontains=search_string)

            # Get jobs that match any of the skills
            jobs = Job.objects.filter(requirements__in=matching_skills).distinct()

            # Prefetch related skills to avoid multiple queries
            jobs = jobs.prefetch_related('requirements')

            # Prepare the data for response
            job_data = []
            for job in jobs:
                # Extract skills associated with the job
                temp_requirements = [requirement.name for requirement in job.requirements.all()]

                # (Serializer can be used) Prepare the job info with skills
                job_info = {
                    'company': job.company,
                    'title': job.title,
                    'location': job.location,
                    'salary': job.salary,
                    'description': job.description,
                    'requirements': temp_requirements
                }

                job_data.append(job_info)

            # Return the unique list of jobs (distinct already handled by the query)
            return Response(job_data)

            

        raise SyntaxError("Invalid type provided")

class FileUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [custom_jwtauthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')  # Extract the file from the request
        username = request.user

        if (not username):
            raise NameError("Username not provided")
            

        if not file:
            raise ValueError("File not provided")

        # Process the PDF file (for example, you could read the contents here)
        try:            
            # Define the file save location
            upload_path = os.path.join(settings.BASE_DIR, 'uploads', username.username + ".pdf")

            # Make sure the directory exists
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            # print("Upload path: ", upload_path)
            # Open the file in 'wb' mode, which will overwrite if it exists
            with open(upload_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            
            # Return a success response
            return Response({"Uploaded File":file.name})
            

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request):
        username = request .user
        action_type = request.GET.get('action_type', None)

        if action_type == 'ai_insights':
            insight_result =  process_file.get_ai_insights(username.username)
            return Response({"ai_insight": insight_result})
        

        if action_type == 'suggest_skills':
            predicted_keywords = process_file.suggest_skills(username.username)
            return Response({"suggest_skills": predicted_keywords})
        

        return Response({"user", "ok"})

class update_applicant_profile(APIView):

    authentication_classes = [custom_jwtauthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        username = request.user
        user_skills_to_be_added = request.data['skills']
        profile_data = request.data

        #Clear Applicant Skills
        username.skills.clear()

        #Debugging
        print("Incoming Profile Data")
        print(profile_data)
        
        print("Skills given")
        print(user_skills_to_be_added)

        print("Skills in database")
        stored_db_skills = [skill.name for skill in Skill.objects.all()]
        print(stored_db_skills)

        #Create objects of non-existing skills
        for incoming_skill in user_skills_to_be_added:
            incoming_skill.strip().lower()
            if incoming_skill not in stored_db_skills:
                Skill.objects.create(name=incoming_skill)
                print("Created: ", incoming_skill)

        #Convert skills to their skill objects
        profile_data['skills'] = [Skill.objects.get(name=skill_name).id for skill_name in user_skills_to_be_added ]
        print("New Profile Data", profile_data)
        
        
        # return Response({"status":"temp ok"})


        #Create serializer for updating profile
        try:
            serializer = GetApplicantProfileSerializer(username, data=profile_data, partial=True)
        except Exception as e:
            print("\n\nSerializer exeptiion", e)


        if serializer.is_valid():
            
            # Save the updated profile data to the database if valid
            serializer.save()
            return Response({'status': 'ok'})
        else:
            print("\n\nSerializer validation error", serializer.errors)
            return Response({'status': 'NOT OK'})
            




class get_skills_applicant(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        skill = Skill.objects.get(name='html')
        skill_applicants = skill.applicants.all()
        applicants = []
        for applicant in skill_applicants:
            applicants.append(applicant.username)
            

        return Response({"Java":applicants})

"""
{
"username":"test1",
"skills":["python","java","html","javascript","css","cpp","c"]
}
"""