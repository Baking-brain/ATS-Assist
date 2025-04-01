"""
URL configuration for djangosrc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.test_view.as_view()),

    #Applicants
    path('api/get_applicants', views.get_applicants.as_view()),
    path('api/create_applicant', views.create_applicant.as_view()),
    path('api/get_profile', views.get_profile.as_view()),
    path('api/add_skills', views.add_skills.as_view()),
    path('api/add_jobs', views.add_jobs.as_view()),
    path('api/get_similar_applicants', views.get_similar_applicants.as_view()),
    path('api/get_similar_jobs', views.get_similar_jobs.as_view()),
    path('api/get_skills_applicant', views.get_skills_applicant.as_view()),
    path('api/get_search_results', views.get_search_results.as_view()),
    path('api/file_upload', views.FileUpload.as_view()),
    path('api/update_applicant_profile', views.update_applicant_profile.as_view()),

    #Log in-out
    path('api/login', views.login.as_view()),
    path('api/logout', views.logout.as_view()),

    #Refresh Token
    path('api/refresh_token', views.refresh_token.as_view()),

    #React
    path('', views.serve_react.as_view()),
    path('dashboard', views.serve_react.as_view()),
    path('search', views.serve_react.as_view()),
    path('profile', views.serve_react.as_view()),

    
]
