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
from .recommendation.cosine_similarity import cos_sim

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

        if not username or not password:
            raise exceptions.ValidationError("Credentials not provided")


        try:
            user = Applicant.objects.get(username=username)

            check_password = user.check_password(password)
            if check_password:
                token = RefreshToken.for_user(user)
                response = Response({"access_token":str(token.access_token), "refresh_token":str(token)})

                response.set_cookie("access_token", str(token.access_token))
                response.set_cookie("refresh_token", str(token))

                return response
            
            else:
                return Response({"status":"missing password or username"}, status=status.HTTP_401_UNAUTHORIZED)

    
        except Exception as e:
            print("\n\nGenerate Error: ",e)
            
            return Response({"Status":"Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)

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

        if not (request.COOKIES.get('access_token') and request.COOKIES.get('access_token')):
            return Response({"status":"no token found"})

        response = Response({"status":"ok"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response

class get_profile(APIView):

    authentication_classes = [custom_jwtauthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        applicant = Applicant.objects.filter(username = request.user)
        applicant = ApplicantSerializer(applicant, many = True).data[0]

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
            print(applicant, similarity_score)
            applicants[applicant] = similarity_score
        
        #Sort according to scores in descending order and filter with score 0 (not at all relevant)
        applicants = dict(sorted(
                                (applicant for applicant in applicants.items() if applicant[1] != 0),
                                key=lambda item: item[1], reverse=True
                                 )
                          )
        
        #Get similar applicants profile
        similar_profiles = []
        for applicant, score in applicants.items():
            temp_profile = GetApplicantProfileSerializer(Applicant.objects.get(username=applicant)).data
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
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        username = request.user
        jobs = JobSerializer(Job.objects.all(), many=True).data



        return Response({"Jobs": jobs})

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
        if search_type == 'applicant':

            applicants = []
            matching_skills = Skill.objects.filter(name__icontains=search_string)
            for skill in matching_skills:
                temp_applicants = ApplicantSerializer(skill.applicants.all(), many=True).data
                for temp_applicant in temp_applicants:

                    temp_skills_index = temp_applicant['skills']
                    temp_skills = []
                    for skill_index in temp_skills_index:
                        temp_skill_name = Skill.objects.get(id=skill_index).name
                        temp_skills.append(temp_skill_name)

                    temp_applicant = {'username': temp_applicant['username'],'skills':temp_skills}
                    applicants.append(temp_applicant)



            #Filter applicants to remove duplicates
            seen_applicants = set()
            filtered_applicants = []
            for applicant in applicants:
                if applicant['username'] not in seen_applicants:
                    filtered_applicants.append(applicant)
                    seen_applicants.add(applicant['username'])

            return Response(filtered_applicants)
        

        #Return search query results for jobs
        elif search_type == 'job' :

            jobs = []
            matching_skills = Skill.objects.filter(name__icontains=search_string)
            for skill in matching_skills:
                temp_jobs = JobSerializer(skill.jobs.all(), many=True).data
                for temp_job in temp_jobs:

                    temp_skills_index = temp_job['requirements']
                    temp_skills = []
                    for skill_index in temp_skills_index:
                        temp_skill_name = Skill.objects.get(id=skill_index).name
                        temp_skills.append(temp_skill_name)

                    temp_job = {'username': temp_job['name'],'skills':temp_skills}
                    jobs.append(temp_job)



            #Filter applicants to remove duplicates
            seen_jobs = set()
            filtered_jobs = []
            for job in jobs:
                if job['username'] not in seen_jobs:
                    filtered_jobs.append(job)
                    seen_jobs.add(job['username'])

            return Response(filtered_jobs)
            

        raise SyntaxError("Invalid type provided")










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