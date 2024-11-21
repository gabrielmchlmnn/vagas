# participante/views.py

import json
from django.shortcuts import redirect, render
from django.http import HttpResponse
from phonenumbers import PhoneNumber
from .models import Participante
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password, check_password
import re
from datetime import date
from phonenumbers import parse, is_valid_number
from dateutil.relativedelta import relativedelta
from sistemaVagas.decorators import login_required, admin_required
from django.contrib.auth.models import User
from django.db.models import Model
from validate_docbr import CPF
from django.http import JsonResponse
from datetime import datetime
from vaga.models import Vaga
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
import locale
from candidatura.models import Candidatura

# Lógica de login
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        senha = request.POST['senha'].strip()
        ultima_tentativa = {'email': email, 'senha': senha}
        request.session['ultima_tentativa'] = ultima_tentativa

        try:
            usuario = autentica_usuario(email, senha, True)
            if usuario:
                request.session['participante_id'] = usuario.id
                request.session['is_superuser'] = True
                return redirect("dashboard")
            else:
                participante = autentica_usuario(email, senha, False)
                if participante:
                    request.session['participante_id'] = participante.id
                    request.session['is_superuser'] = False
                    return redirect("vagas")
                else:
                    raise Exception('Credenciais inválidas!')
        except Exception as e:
            messages.error(request, f'{e}')
            return redirect('login')
    else:
        ultima_tentativa = request.session.get('ultima_tentativa', {})
        context = {
            'nome': ultima_tentativa.get('nome', ''),
            'cpf': ultima_tentativa.get('cpf', ''),
            'celular': ultima_tentativa.get('celular', ''),
            'codigo_pais': ultima_tentativa.get('codigoPais', ''),
            'email': ultima_tentativa.get('email', ''),
            'senha': ultima_tentativa.get('senha', ''),
            'confirm_senha': ultima_tentativa.get('confirm_senha', ''),
            'data_nascimento': ultima_tentativa.get('data_nascimento', '')
        }
        return render(request, 'participante/login.html', context=context)

@login_required
@admin_required
def dashboard(request):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    vagas_por_mes = (
        Vaga.objects
        .annotate(mes=TruncMonth('dataPublicacao'))
        .values('mes')
        .annotate(quantidade=Count('id'))
        .order_by('mes')
    )
    candidaturas_por_mes = (
        Candidatura.objects
        .annotate(mes=TruncMonth('dataInscricao'))
        .values('mes')
        .annotate(quantidade=Count('id'))
        .order_by('mes')
    )

    dados_vagas = [
        {
            'mes': mes_data['mes'].strftime('%B/%Y').capitalize(),
            'quantidade': mes_data['quantidade']
        }
        for mes_data in vagas_por_mes
    ]

    dados_candidaturas = [
        {
            'mes': mes['mes'].strftime('%B/%Y').capitalize(),
            'quantidade': mes['quantidade']
        }
        for mes in candidaturas_por_mes
    ]

    context = {
        'dados_vagas': json.dumps(dados_vagas),
        'dados_candidaturas': json.dumps(dados_candidaturas),
        'superUser': True
    }
    return render(request, 'dashboard.html', context=context)

def logon_view(request):
    if request.method == 'POST':
        nome = request.POST['nome'].strip()
        cpf = request.POST['cpf'].strip()
        celular = request.POST['celular'].strip()
        codigo_pais = request.POST['codigoPais'].strip()
        email = request.POST['email'].strip()
        senha = request.POST['senha'].strip()
        confirm_senha = request.POST['confirm_senha'].strip()
        data_nascimento = request.POST['data_nascimento'].strip()
        indicador_pcd = request.POST['indicadorPCD'].strip() == 'True'

        ultima_tentativa_logon = {
            'nome': nome,
            'cpf': cpf,
            'celular': celular,
            'codigo_pais': codigo_pais,
            'email': email,
            'senha': senha,
            'confirm_senha': confirm_senha,
            'data_nascimento': data_nascimento,
            'indicador_pcd':indicador_pcd
        }
        request.session['ultima_tentativa_logon'] = ultima_tentativa_logon

        try:
            celular = celular.replace(' ', '')
            if nome.isdigit():
                raise Exception('Nome inválido!')
            if len(celular) != 14:
                raise Exception('Celular inválido!')

            if senha != confirm_senha:
                raise Exception('As senhas não coincidem!')

            if Participante.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
                raise Exception('Email já cadastrado!')

            if not CPF().validate(cpf):
                raise Exception('CPF inválido!')

            cpf = re.sub(r'[.-]', '', cpf)
            if Participante.objects.filter(cpf=cpf).exists():
                raise Exception('CPF já cadastrado!')

            data_nascimento = parse_date(data_nascimento)
            if relativedelta(date.today(), data_nascimento).years < 14:
                raise Exception('A idade mínima para cadastro é 14 anos!')

            celular_formatado = f"+{codigo_pais}{re.sub(r'[()-]', '', celular)}"

            # Cria o novo participante
            Participante.objects.create(
                nome=nome,
                cpf=cpf,
                celular=celular_formatado,
                email=email,
                senha=make_password(senha),
                dataNascimento=data_nascimento,
                indicadorPCD=indicador_pcd
            )
            messages.success(request, 'Cadastro realizado com sucesso!')
            request.session['ultima_tentativa_logon'] = ''
            return redirect('login')
        except Exception as e:
            messages.error(request, f'{e}')
            return redirect('logon')
    else:
        ultima_tentativa_logon = request.session.get('ultima_tentativa_logon', {})
        context = {
            'nome': ultima_tentativa_logon.get('nome',''),
            'cpf': ultima_tentativa_logon.get('cpf'),
            'celular': ultima_tentativa_logon.get('celular'),
            'codigo_pais': ultima_tentativa_logon.get('codigo_pais'),
            'email': ultima_tentativa_logon.get('email'),
            'senha': ultima_tentativa_logon.get('senha'),
            'confirm_senha': ultima_tentativa_logon.get('confirm_senha'),
            'data_nascimento': ultima_tentativa_logon.get('data_nascimento')
        }
        return render(request, 'participante/logon.html', context=context)

def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('login')

def autentica_usuario(email: str, senha: str, is_superuser: bool):
    try:
        if is_superuser:
            usuario = User.objects.get(email=email)
            senha_salva = usuario.password
        else:
            usuario = Participante.objects.get(email=email)
            senha_salva =  usuario.senha    
        
        if check_password(senha, senha_salva):
            return usuario
        return None
    except Exception:
        return None
