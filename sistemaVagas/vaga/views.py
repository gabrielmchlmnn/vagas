from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count
from django.urls import reverse
from datetime import date
from .models import Vaga
from sistemaVagas.functions import aplicaFiltrosVaga, filtrosVaga
from django.views.decorators.csrf import csrf_exempt
from sistemaVagas.decorators import login_required,admin_required
# Exibe a lista de vagas
def listar_vagas(request):
    sessao_ativa = 'participante_id' in request.session
    superusuario = request.session.get('is_superuser', False)
    vagas = Vaga.objects.filter(aplicaFiltrosVaga(request)).annotate(qtd_participantes=Count('candidatura'))
    filtros = filtrosVaga(request)
    context = {
        'vagas': vagas,
        "modalidades": Vaga.Modalidade.choices,
        "faixa_salarios": Vaga.FaixasSalario.choices,
        "escolaridades": Vaga.Escolaridade.choices,
        'sessao': sessao_ativa,
        'superUser': superusuario,
        'filtros': filtros
    }
    return render(request, 'vagas/vagas.html', context)

# Cadastra uma nova vaga
@login_required
@admin_required
def cadastrar_vaga(request):
    if request.method == 'POST':
        descricao = request.POST['descricao'].strip()
        faixa_salarial = request.POST['faixaSalarial'].strip()
        requisitos = request.POST['requisitos'].strip()
        escolaridade = request.POST['escolaridade'].strip()
        modalidade = request.POST['modalidade'].strip()
        indicador_pcd = request.POST['indicadorPCD'].strip() == 'True'

        try:
            vaga = Vaga(
                descricao=descricao,
                faixaSalarial=faixa_salarial,
                requisitos=requisitos,
                escolaridade=escolaridade,
                modalidade=modalidade,
                indicadorPCD=indicador_pcd,
                ativo=True,  
                dataPublicacao=date.today(),
            )
            vaga.save()
            messages.success(request, "Vaga cadastrada com sucesso!")
            return redirect(reverse('vagas'))
        except Exception as e:
            messages.error(request, "Não foi possível cadastrar esta vaga!")
            return redirect(reverse('vagas'))
    else:
        return redirect(reverse('vagas'))

# Filtra as vagas com base nos parâmetros fornecidos
@csrf_exempt
def filtrar_vagas(request):
    sessao_ativa = 'participante_id' in request.session
    superusuario = request.session.get('is_superuser', False)

    if request.method == 'GET':
        vagas = Vaga.objects.filter(aplicaFiltrosVaga(request)).annotate(qtd_participantes=Count('candidatura'))
        context = {
            'vagas': vagas,
            'superUser': superusuario,
            'sessao': sessao_ativa,
            "modalidades": Vaga.Modalidade.choices,
            "faixa_salarios": Vaga.FaixasSalario.choices,
            "escolaridades": Vaga.Escolaridade.choices
        }
        vagas_html = render_to_string('vagas/listaVagas.html', context=context)

        return JsonResponse({'vagas': vagas_html})
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

# Inativa uma vaga existente
@login_required
@admin_required
def inativar_vaga(request, id):
    try:
        vaga = Vaga.objects.get(id=id)
        vaga.inativar()
        messages.success(request, "Vaga inativada com sucesso!")
        return redirect(reverse('vagas'))
    except Vaga.DoesNotExist:
        messages.error(request, "Vaga não encontrada!")
        return redirect(reverse('vagas'))
    except Exception as e:
        messages.error(request, f"Erro ao inativar vaga: {e}")
        return redirect(reverse('vagas'))

# Edita uma vaga existente
@login_required
@admin_required
def editar_vaga(request, id):
    if request.method == 'POST':
        try:
            descricao = request.POST['descricao'].strip()
            faixa_salarial = request.POST['faixaSalarial'].strip()
            requisitos = request.POST['requisitos'].strip()
            escolaridade = request.POST['escolaridade'].strip()
            modalidade = request.POST['modalidade'].strip()
            
            Vaga.objects.filter(id=id).update(
                descricao=descricao,
                faixaSalarial=faixa_salarial,
                requisitos=requisitos,
                escolaridade=escolaridade,
                modalidade=modalidade
            )
            messages.success(request, "Vaga editada com sucesso!")
            return redirect(reverse('vagas'))
        except Vaga.DoesNotExist:
            messages.error(request, "Vaga não encontrada!")
            return redirect(reverse('vagas'))
        except Exception as e:
            messages.error(request, f"Erro ao editar vaga: {e}")
            return redirect(reverse('vagas'))
    else:
        return redirect(reverse('vagas'))
