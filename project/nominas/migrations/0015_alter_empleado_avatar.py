# Generated by Django 5.1.1 on 2024-09-30 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominas', '0014_alter_empleado_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatares'),
        ),
    ]
