from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class test_view(APIView):
    def get(self, request, *kwargs, **args):
        return Response({"Server":"Running"},status=200)
