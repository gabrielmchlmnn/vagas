from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from . import views


urlpatterns = [

    path('candidatura/<int:id>/', views.cadastroCandidatura, name='cadastro_candidatura')

]