# Generated by Django 2.0.2 on 2018-07-04 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupoparticipante',
            options={'ordering': ('descricao',), 'verbose_name': 'Grupo de Participante', 'verbose_name_plural': 'Grupos de Participantes'},
        ),
        migrations.AlterModelOptions(
            name='regiaodevenda',
            options={'ordering': ('descricao',), 'verbose_name': 'Região de Venda', 'verbose_name_plural': 'Regiões de Vendas'},
        ),
        migrations.AlterField(
            model_name='participante',
            name='inscricao_municipal',
            field=models.CharField(blank=True, default='ISENTO', max_length=15, verbose_name='Inscrição Municipal'),
        ),
    ]
