# Generated by Django 4.1.3 on 2022-12-12 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0008_pagamento_valorpagamentoservico_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='dataPagamento',
            field=models.DateField(verbose_name='dataPagamento'),
        ),
    ]
