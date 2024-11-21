from django.db import models
from django.utils.timezone import now
from participante.models import Participante
from vaga.models import Vaga

class Candidatura(models.Model):
    class Escolaridade(models.IntegerChoices):
        FUNDAMENTAL = 1, 'Ensino fundamental'
        TECNOLOGO = 2, 'Tecnólogo'
        SUPERIOR = 3, 'Ensino superior'
        MESTRADO = 4, 'Pós/MBA/Mestrado'
        DOUTORADO = 5, 'Doutorado'
    
    class Status(models.IntegerChoices):
        INSCRITO = 1, 'Inscrito'
        EMANÁLISE = 2, 'Em análise'
        SELECIONADO = 3, 'Selecionado'
        REJEITADO = 4, 'Rejeitado'
    
    participanteId = models.ForeignKey(Participante, on_delete=models.CASCADE)
    vagaId = models.ForeignKey(Vaga, on_delete=models.CASCADE)
    pretensaoSalarial = models.DecimalField(max_digits=10, decimal_places=2)
    escolaridade = models.IntegerField(choices=Escolaridade,default=1)
    pontos = models.FloatField(default=0)
    dataInscricao = models.DateTimeField(default=now)
    status = models.IntegerField(choices=Status, default=1)
    experiencia = models.TextField(blank=True, null=True)
    pcd = models.BooleanField(default=False)
    disponibilidadeImediata = models.BooleanField(default=False)

    def __str__(self):
        return f"Candidatura de {self.participanteId.nome} - Vaga {self.vagaId}"
    
    def format_pretensao_salarial(self):
        return f"{self.pretensaoSalarial:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    def format_pontos(self):
        return int(self.pontos)