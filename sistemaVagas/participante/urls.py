from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logon/', views.logon_view, name='logon'),
    path('logout/', views.logout_view, name='logout'),
]
