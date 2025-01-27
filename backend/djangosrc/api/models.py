from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class ApplicantManager(BaseUserManager):
    def create_user(self, username, password):
        applicant = self.model(username = username)
        applicant.set_password(password)
        applicant.save(using=self._db)

        return applicant
    
    def create_superuser(self, username, password):
        return self.create_user(username, password)



class Applicant(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'

    objects = ApplicantManager()