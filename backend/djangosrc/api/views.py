from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from .serializers import ApplicantSerializer, SkillSerializer, GetApplicantSkillsSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from .authentication import custom_jwtauthentication
from rest_framework.permissions import IsAuthenticated
from .models import Applicant, Skill
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

        return Response({"Applicants":applicants})

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