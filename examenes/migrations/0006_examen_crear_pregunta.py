# Generated by Django 3.0.4 on 2020-03-31 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examenes', '0005_examen_opcional'),
    ]

    operations = [
        migrations.AddField(
            model_name='examen',
            name='crear_pregunta',
            field=models.TextField(blank=True, default='', max_length=10000),
        ),
    ]