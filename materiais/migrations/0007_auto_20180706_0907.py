# Generated by Django 2.0.2 on 2018-07-06 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiais', '0006_auto_20180706_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidowebitem',
            name='codigo_ncm',
            field=models.CharField(max_length=100),
        ),
    ]
