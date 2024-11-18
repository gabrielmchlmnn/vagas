from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('inicial/', views.inicial_page, name='inicial_page'),
    path('logon/', views.logon_view, name='logon'),
    path('logout/', views.logout_view, name='logout'),
]
