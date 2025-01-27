from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from .serializers import ApplicantSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .authentication import custom_jwtauthentication
from rest_framework.permissions import IsAuthenticated
from .models import Applicant

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
            if user and check_password:
                token = RefreshToken.for_user(user)
                response = Response({"access_token":str(token.access_token), "refresh_token":str(token)})

                response.set_cookie("access_token", str(token.access_token))
                response.set_cookie("refresh_token", str(token))

                return response
            
            else:
                return Response({"status":"wrong password or user"})

    
        except Exception as e:
            print("\n\nGenerate Error: ",e)
            
            return Response({"Status":"Something went wrong"}, status=status.HTTP_401_UNAUTHORIZED)

class refresh_token(APIView):
    
    authentication_classes = [custom_jwtauthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            new_token = RefreshToken(request.COOKIES.get('refresh_token'))
            
            response = Response({"access_token":str(new_token.access_token), "refresh_token":str(new_token)})
            response.set_cookie("access_token", new_token.access_token)
            response.set_cookie("refresh_token", new_token)

            return response

        except Exception as e:
            print(f'\n\nError => {e}\n\n')
            return Response({"status":"Refresh token expired"})

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




