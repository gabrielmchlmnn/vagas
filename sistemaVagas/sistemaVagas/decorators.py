# core/decorators.py
from django.shortcuts import redirect
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        participante_id = request.session.get('participante_id')
        if not participante_id:
            return redirect('login')  # Redireciona para a página de login
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        adminSession = request.session.get('is_superuser')
        if adminSession == False:
            return redirect('vagas') 
        return view_func(request, *args, **kwargs)
    return _wrapped_view
