from django.urls import path
from . import views

urlpatterns = [
    path('vagas/', views.vagas, name='vagas'),
    path('cadastrar-vagas/', views.cadastrarVaga, name='cadastroVaga'),
]