from rest_framework import serializers
from .models import Applicant, Skill

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = "__all__"



class GetApplicantSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['username', 'skills']



class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"