# Generated by Django 3.2.8 on 2021-12-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0045_notificaciones_creado_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificaciones',
            name='comentario',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notificaciones',
            name='me_gusta',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notificaciones',
            name='no_megusta',
            field=models.BooleanField(default=False),
        ),
    ]
