# Generated by Django 3.2.8 on 2021-12-18 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0049_comentario_nombre_comentador'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='desaprobado',
            field=models.BooleanField(default=False),
        ),
    ]
