from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count,Prefetch
from django.urls import reverse
from datetime import date
from candidatura.models import Candidatura
from .models import Vaga
from sistemaVagas.functions import aplicaFiltrosVaga, filtrosVaga
from sistemaVagas.decorators import login_required,admin_required
from django.http import QueryDict

# teste
# Exibe a lista de vagas
def listar_vagas(request):
    sessao_ativa = 'participante_id' in request.session
    superusuario = request.session.get('is_superuser', False)
    vagas = Vaga.objects.filter(aplicaFiltrosVaga(request)
            ).annotate(qtd_participantes=Count('candidatura')
            ).prefetch_related(
                Prefetch('candidatura_set', queryset=Candidatura.objects.select_related('participanteId'))
            )

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
    filtros = filtrosVaga(request)      
    query_params = QueryDict(mutable=True)
    query_params.update(filtros)
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
            # Redirecionar com os filtros na URL
            return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
        except Exception as e:
            messages.error(request, "Não foi possível cadastrar esta vaga!")
            return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
    else:
        return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
# Inativa uma vaga existente
@login_required
@admin_required
def inativar_vaga(request, id):
    filtros = filtrosVaga(request)      
    query_params = QueryDict(mutable=True)
    query_params.update(filtros)
    try:
        vaga = Vaga.objects.get(id=id)
        vaga.inativar()
        messages.success(request, "Vaga inativada com sucesso!")
        # Redirecionar com os filtros na URL
        return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
    except Vaga.DoesNotExist:
        messages.error(request, "Vaga não encontrada!")        
        return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
    except Exception as e:
        messages.error(request, f"Erro ao inativar vaga: {e}")
        return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
    
# Edita uma vaga existente
@login_required
@admin_required
def editar_vaga(request, id):
    filtros = filtrosVaga(request)   
    query_params = QueryDict(mutable=True)
    query_params.update(filtros)   
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
            # Redirecionar com os filtros na URL
            return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
        
        except Vaga.DoesNotExist:
            messages.error(request, "Vaga não encontrada!")
            return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")        
        
        except Exception as e:
            messages.error(request, f"Erro ao editar vaga: {e}")
            return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
    else:
        return redirect(f"{reverse('vagas')}?{query_params.urlencode()}")
