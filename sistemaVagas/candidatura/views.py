from django.shortcuts import redirect
from sistemaVagas.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from vaga.models import Vaga
from .models import Candidatura
from django.db.models import Q
from participante.models import Participante


@login_required
def cadastroCandidatura(request,id):
    if request.method == 'POST':
        idParticipante = request.session.get('participanteId')
        ultimaEscolaridade = request.POST.get('ultimaEscolaridade').strip()
        pretensaoSalarial = request.POST.get('pretensaoSalarial').strip()
        experiencia = request.POST.get('experiencia').strip()
        disponivel = request.POST.get('disponivel', False)
        pontos = 0
        try:   
            vaga = Vaga.objects.get(id=id)
            participante = Participante.objects.get(id=idParticipante)
            
            pretensaoSalarial = pretensaoSalarial.replace('R$ ','').replace('.','').replace(',','.')

            if vaga.verificaSalario(float(pretensaoSalarial)):
                pontos += 1

            if int(ultimaEscolaridade) >= vaga.escolaridade:
                pontos += 1
            
            if disponivel:
                pontos += 1

            if vaga.indicadorPCD == 1 and participante.indicadorPCD == 1:
                pontos += 1
            
            if vaga.indicadorPCD == 0 and participante.indicadorPCD == 1:
                raise Exception("Esta vaga não se encontra disponível para PCD!")

            candidatura_existente = Candidatura.objects.filter(
                    Q(participanteId=participante) &
                    Q(vagaId=vaga)
            ).exists()

            if candidatura_existente:
                raise Exception("Você já está cadastrado nessa vaga!")

            candidatura = Candidatura(
                participanteId=participante,
                vagaId=vaga,
                pretensaoSalarial=pretensaoSalarial,
                escolaridade=ultimaEscolaridade,
                pontos=pontos,
                experiencia=experiencia,
                pcd=participante.indicadorPCD,
                status=1,
                disponibilidadeImediata=disponivel
            )
            candidatura.save()
            messages.success(request,"Candidatura feita com sucesso!")
            return redirect(reverse('vagas'))

        except Exception as e:
            messages.error(request,f"{str(e)}")
            return redirect(reverse('vagas'))
    else:
        return redirect(reverse('vagas'))



