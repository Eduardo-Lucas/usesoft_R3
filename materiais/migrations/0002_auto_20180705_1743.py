# Generated by Django 2.0.2 on 2018-07-05 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiais', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produtotributacao',
            options={'verbose_name': 'Produto Tributação', 'verbose_name_plural': 'Produtos Tributações'},
        ),
        migrations.AlterField(
            model_name='produtotributacao',
            name='situacao_tributaria_icms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='situacaotributariaicms', to='globais.SituacaoTribIcms'),
        ),
        migrations.AlterField(
            model_name='produtotributacao',
            name='situacao_tributaria_pis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globais.SituacaoTribPis'),
        ),
    ]
