from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Vaga
from datetime import date
# Create your views here.
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

def vagas(request):

    sessao = 'participanteId' in request.session
    superUser = request.session.get('isSuperUser', False)

    vagas = Vaga.objects.all()
    context = {
        'vagas':vagas,
        'sessao':sessao,
        'superUser' : superUser
    }
    return render(request, 'vagas/vagas.html',context=context)


@csrf_exempt
def cadastrarVaga(request):
    print(request.method)
    if request.method == 'POST':
        descricao = request.POST['descricao'].strip()
        faixaSalarial = request.POST['faixaSalarial'].strip()
        requisitos = request.POST['requisitos'].strip()
        escolaridade = request.POST['escolaridade'].strip()
        modalidade = request.POST['modalidade'].strip()
        indicadorPcd = request.POST['indicadorPCD'].strip() == 'True'

        try:    
            vaga = Vaga(
                descricao=descricao,
                faixaSalarial=faixaSalarial,
                requisitos=requisitos,
                escolaridade=escolaridade,
                modalidade=modalidade,
                indicadorPCD=indicadorPcd,
                ativo=True,  
                dataPublicacao=date.today(),
            )
            vaga.save()
            vagas = Vaga.objects.filter(ativo=True).values(
                'descricao', 'faixaSalarial', 'requisitos',
                'escolaridade', 'modalidade', 'indicadorPCD',
                'dataPublicacao'
            )
            vagas_html = render_to_string('vagas/listaVagas.html', {'vagas': vagas})

            return JsonResponse({
                'mensagem': 'Vaga criada com sucesso!',
                'vagas': vagas_html
            })

        except Exception as e:
            print(e)
            messages.error(request,'Não foi possível cadastrar a vaga')            
            return JsonResponse({'erro': 'Não foi possível cadastrar a vaga'}, status=405)

    else:
        vagas = Vaga.objects.filter(ativo=True).values(
            'descricao', 'faixaSalarial', 'requisitos',
            'escolaridade', 'modalidade', 'indicadorPCD',
            'dataPublicacao'
        )
        vagas_html = render_to_string('vagas/listaVagas.html', {'vagas': vagas})

        return render(request, 'vagas/vagas.html',context={'vagas':vagas_html})

