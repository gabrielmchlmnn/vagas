from django.urls import path
from . import views

urlpatterns = [
    path('listar-vagas/', views.listar_vagas, name='vagas'),
    path('cadastrar-vaga/', views.cadastrar_vaga, name='cadastrar_vaga'),
    path('inativar-vaga/<int:id>/', views.inativar_vaga, name='inativar_vaga'),
    path('editar-vaga/<int:id>/', views.editar_vaga, name='editar_vaga'),
]
