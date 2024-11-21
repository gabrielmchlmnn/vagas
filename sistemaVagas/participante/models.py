from django.db import models
from django.forms import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password,check_password

# Create your models here.
class Participante(models.Model):
    nome = models.CharField(max_length=70)
    cpf = models.CharField(max_length=11)
    celular = PhoneNumberField()
    email = models.CharField(unique=True,max_length=256)
    senha = models.CharField(max_length=128)  
    dataNascimento = models.DateField()
    dataAlteracao = models.DateTimeField(auto_now=True)  
    indicadorPCD = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
    def set_senha(self, senhaDigitada):
        self.senha = make_password(senhaDigitada)
    
    def check_password(self, senhaDigitada):
        return check_password(senhaDigitada, self.senha)

    def format_cpf(self):
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"