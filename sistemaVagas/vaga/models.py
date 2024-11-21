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

    def getSalario(self):
        """Retorna o valor mínimo da faixa salarial da vaga."""
        if self.faixaSalarial == self.FaixasSalario.ATÉ_1000:
            return 1000
        elif self.faixaSalarial == self.FaixasSalario.DE_1000_A_2000:
            return 1000
        elif self.faixaSalarial == self.FaixasSalario.DE_2000_A_3000:
            return 2000
        elif self.faixaSalarial == self.FaixasSalario.ACIMA_DE_3000:
            return 3000
        return 0  # Caso não esteja em nenhuma faixa (não é comum)
    
    def verificaSalario(self, valor: float):
        valorMinFaixa = self.getSalario()
        if valor <= valorMinFaixa:
            return 1
        else:
            return 0
        
    def inativar(self):
        """
        Método para inativar a vaga.
        Define 'ativo' como False e 'dataInativacao' como a data atual.
        """
        if self.ativo:  # Apenas inativa se a vaga estiver ativa
            self.ativo = False
            self.dataInativacao = date.today()
            self.save()  # Salva as alterações no banco de dados
            return True
        return False  # Retorna False se a vaga já estiver inativa