from django.shortcuts import redirect, render
from django.http import HttpResponse
from phonenumbers import PhoneNumber
from .models import Participante
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password,check_password
import re
from datetime import date
from phonenumbers import parse, is_valid_number
from dateutil.relativedelta import relativedelta
from sistemaVagas.decorators import login_required  # Importa o decorador
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Model
from validate_docbr import CPF
# Create your views here.


def login_view(request):
    request.session['ultimaTentativaLogon'] = ''
    if request.method == 'POST':
        # Lógica para processar o login
        email = request.POST['email']
        senha = request.POST['senha']
        ultimaTentativa = {
            'email':email ,
            'senha':senha
        }
        request.session['ultimaTentativa'] = ultimaTentativa   
        try:
            # Verifica se o e-mail existe no banco
            participante = autenticaModelo(Participante,email,senha) 
            if participante is not None:
                request.session['participanteId'] = participante.id
                request.session['isSuperUser'] = False
                return redirect("inicial_page")
            else:
                # Caso não seja um Participante, tenta autenticar no modelo User
                usuario = autenticaModelo(User,email,senha)
                if usuario is not None:
                    request.session['participanteId'] = usuario.id
                    request.session['isSuperUser'] = True
                    return redirect("inicial_page")
                else:
                    # Nenhum dos modelos foi autenticado
                    messages.error(request, 'Credenciais inválidas!')
                    return redirect("login")
        except Exception as e:
            print(f"Erro ao efetuar login --> {e}")
            messages.error(request, 'Não foi possível efetuar o login!')
            return redirect("login")
    else:
        ultimaTentativa = request.session.get('ultimaTentativa', {})
        context = {}
        if isinstance(ultimaTentativa, dict):
            context = {
                'nome': ultimaTentativa.get('nome'),
                'cpf': ultimaTentativa.get('cpf'),
                'celular': ultimaTentativa.get('celular'),
                'codigoPais': ultimaTentativa.get('codigoPais'),
                'email': ultimaTentativa.get('email'),
                'senha': ultimaTentativa.get('senha'),
                'confirmSenha': ultimaTentativa.get('confirmSenha'),
                'dataNascimento': ultimaTentativa.get('dataNascimento')
            }
        return render(request, 'participante/login.html',context=context)

@login_required
def inicial_page(request):
    return render(request, 'participante/index.html')


def logon_view(request):
    request.session['ultimaTentativa'] = ''
    if request.method == 'POST':
        # Lógica para processar o logon
        nome = request.POST['nome'].strip()
        cpf = request.POST['cpf'].strip()
        celular = request.POST['celular'].replace(' ','')
        codigoPais = request.POST['codigoPais'].strip()
        email = request.POST['email'].strip()
        senha = request.POST['senha'].strip()
        confirmSenha = request.POST['confirmSenha'].strip()
        dataNascimento = request.POST['dataNascimento'].strip()
        ultimaTentativaLogon = {
            'nome':nome,
            'cpf':cpf ,
            'celular':celular ,
            'codigoPais':codigoPais ,
            'email':email ,
            'senha':senha ,
            'confirmSenha':confirmSenha,
            'dataNascimento':dataNascimento
        }
        request.session['ultimaTentativaLogon'] = ultimaTentativaLogon   
     
        if senha != confirmSenha:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('logon')
        
        participantes = Participante.objects.filter(email=email)

        if participantes.exists():
            messages.error(request, 'Email já cadastrado!')
            return redirect('logon')
        
        validation = CPF()
        if validation.validate(cpf) == False:
            messages.error(request, 'CPF inválido!')
            return redirect('logon')

        cpf = re.sub(r'[.-]', '', cpf)  
        participantes = Participante.objects.filter(cpf=cpf)

        if participantes.exists():
            messages.error(request, 'CPF já cadastrado!')
            return redirect('logon')
        

        data_atual = date.today()
        dataNascimento = parse_date(dataNascimento)
        if (relativedelta(data_atual, dataNascimento).years < 14):
            messages.error(request, 'A idade mínima para cadastro é 14 anos!')
            return redirect('logon')
        try:
            # Formatar o número do celular corretamente
            celular = re.sub(r'[()-]', '', celular)  
            celularFormatado = f"+{codigoPais}{celular}"

            # Criar o novo participante
            Participante.objects.create(
                nome=nome,
                cpf=cpf,
                celular=celularFormatado,
                email=email,
                senha=make_password(senha), 
                dataNascimento=dataNascimento
            )
            messages.success(request, 'Cadastro realizado com sucesso!')
            request.session['ultimaTentativaLogon'] = ''
            return redirect('login')  # Redireciona para a página de login após o cadastro
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao criar participante: {e}')           
            return redirect('logon')
    else:
        ultimaTentativaLogon = request.session.get('ultimaTentativaLogon')
        context = {}

        if isinstance(ultimaTentativaLogon, dict):
            context = {
                'nome': ultimaTentativaLogon.get('nome'),
                'cpf': ultimaTentativaLogon.get('cpf'),
                'celular': ultimaTentativaLogon.get('celular'),
                'codigoPais': ultimaTentativaLogon.get('codigoPais'),
                'email': ultimaTentativaLogon.get('email'),
                'senha': ultimaTentativaLogon.get('senha'),
                'confirmSenha': ultimaTentativaLogon.get('confirmSenha'),
                'dataNascimento': ultimaTentativaLogon.get('dataNascimento')
            }

        return render(request, 'participante/logon.html',context=context)


def logout_view(request):
    if 'participanteId' in request.session:
        del request.session['participanteId']
    if 'ultimaTentativa' in request.session:
        del request.session['ultimaTentativa']
    return redirect('login')  


def autenticaModelo(modelo: Model, email: str, senha: str):
    try:
        # Nome do modelo (para depuração)
        print(f"Modelo: {modelo.__name__}")    
        print(f"Email: {email}")

        # Busca o objeto pelo e-mail
        entidade = modelo.objects.get(email=email)
        print("caiu 1")

        # Identifica o campo correto para a senha
        senhaSalva = entidade.password if modelo.__name__ == 'User' else entidade.senha

        # Verifica a senha
        if check_password(senha, senhaSalva):
            return entidade
        else:
            print("caiu 2")
            return None

    except modelo.DoesNotExist:
        print("Email não encontrado.")
        return None

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
