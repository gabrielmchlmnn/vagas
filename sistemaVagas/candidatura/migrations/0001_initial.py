# Generated by Django 5.1.3 on 2024-11-19 04:27

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participante', '0001_initial'),
        ('vaga', '0006_alter_vaga_faixasalarial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pretensaoSalarial', models.DecimalField(decimal_places=2, max_digits=10)),
                ('escolaridade', models.IntegerField(choices=[(1, 'Ensino fundamental'), (2, 'Tecnólogo'), (3, 'Ensino superior'), (4, 'Pós/MBA/Mestrado'), (5, 'Doutorado')], default=1)),
                ('pontos', models.FloatField(default=0)),
                ('dataInscricao', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(choices=[(1, 'Inscrito'), (2, 'Em análise'), (3, 'Selecionado'), (4, 'Rejeitado')], default=1)),
                ('cartaApresentacao', models.TextField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('pcd', models.BooleanField(default=False)),
                ('disponibilidadeViagem', models.BooleanField(default=False)),
                ('participante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='participante.participante')),
                ('vagaId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaga.vaga')),
            ],
        ),
    ]