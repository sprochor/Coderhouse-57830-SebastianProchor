# Generated by Django 5.1.1 on 2024-09-30 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominas', '0013_empleado_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatares'),
        ),
    ]
