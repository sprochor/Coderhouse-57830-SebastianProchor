# Generated by Django 5.1.1 on 2024-09-20 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominas', '0007_remove_liquidacion_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liquidacion',
            name='fecha_pago',
            field=models.DateField(),
        ),
    ]
