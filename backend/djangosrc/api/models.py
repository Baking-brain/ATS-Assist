from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class ApplicantManager(BaseUserManager):
    def create_user(self, username, password, name):
        applicant = self.model(username = username, name = name)
        applicant.set_password(password)
        applicant.save(using=self._db)

        return applicant
    
    def create_superuser(self, username, password, name):
        return self.create_user(username, password, name)
    


class Skill(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name



class Applicant(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30, default="")
    password = models.CharField(max_length=128)
    skills = models.ManyToManyField(Skill, related_name='applicants')
    experience = models.FloatField(default=0)
    education = models.CharField(max_length=100, default="")
    about = models.TextField(default="")
    email = models.EmailField(max_length=255)
    location = models.CharField(max_length=255, default="")

    USERNAME_FIELD = 'username'

    objects = ApplicantManager()

    def __str__(self):
        return self.username



class Job(models.Model):
    company = models.CharField(max_length=100, default="Generic Company")
    requirements = models.ManyToManyField(Skill, related_name='jobs')
    title = models.CharField(max_length=100, default=None)
    location = models.CharField(max_length=100, default=None)
    salary = models.FloatField(default=None)
    description = models.CharField(max_length=250, default="")


    def __str__(self):
        return self.name

