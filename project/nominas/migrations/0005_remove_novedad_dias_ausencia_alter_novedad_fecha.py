# Generated by Django 5.1.1 on 2024-09-17 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominas', '0004_remove_novedad_horas_extras_100_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novedad',
            name='dias_ausencia',
        ),
        migrations.AlterField(
            model_name='novedad',
            name='fecha',
            field=models.DateField(),
        ),
    ]
