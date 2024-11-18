from django.db import models
from datetime import date

# Create your models here.

class Vaga(models.Model):

    class Modalidade(models.IntegerChoices):
        PRESENCIAL = 1, 'Presencial'
        HIBRIDA = 2, 'Híbrida'
        REMOTO = 3, 'Remoto'

    class FaixasSalario(models.IntegerChoices):
        ATÉ_1000 = 1, 'Até R$1.000'
        DE_1000_A_2000 = 2, 'De R$1.000 à R$2.000'
        DE_2000_A_3000 = 3, 'De R$2.000 à R$3.000'
        ACIMA_DE_3000 = 4, 'Acima de R$3.000'

    class Escolaridade(models.IntegerChoices):
        FUNDAMENTAL = 1, 'Ensino fundamental'
        TECNOLOGO = 2, 'Tecnólogo'
        SUPERIOR = 3, 'Ensino superior'
        MESTRADO = 4, 'Pós/MBA/Mestrado'
        DOUTORADO = 5, 'Doutorado'

    descricao = models.CharField(max_length=80)
    faixaSalarial = models.IntegerField(choices=FaixasSalario,default=1)
    requisitos = models.TextField()
    escolaridade = models.IntegerField(choices=Escolaridade)
    modalidade = models.IntegerField(choices=Modalidade,default=1)
    indicadorPCD = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    dataInativacao = models.DateField(null=True, blank=True, default=None)
    dataPublicacao = models.DateField(default=date.today)
    def __str__(self):
        return self.descricao

