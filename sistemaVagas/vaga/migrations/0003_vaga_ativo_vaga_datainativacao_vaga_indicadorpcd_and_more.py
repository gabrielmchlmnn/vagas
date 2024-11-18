# Generated by Django 5.1.3 on 2024-11-18 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaga', '0002_vaga_datapublicacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaga',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='vaga',
            name='dataInativacao',
            field=models.DateField(null=True, blank=True, default=None),
        ),
        migrations.AddField(
            model_name='vaga',
            name='indicadorPCD',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vaga',
            name='modalidade',
            field=models.IntegerField(choices=[(1, 'Presencial'), (2, 'Híbrida'), (3, 'Remoto')], default=1),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='escolaridade',
            field=models.IntegerField(choices=[(1, 'Ensino fundamental'), (2, 'Tecnólogo'), (3, 'Ensino superior'), (4, 'Pós/MBA/Mestrado'), (5, 'Doutorado')]),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='faixaSalarial',
            field=models.IntegerField(choices=[(1, 'Até 1.000'), (2, 'De 1.000 à 2.000'), (3, 'De 2.000 à 3.000'), (4, 'Acima de 3.000')], default=1),
        ),
    ]