# Generated by Django 3.2.8 on 2021-12-05 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0046_auto_20211205_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificaciones',
            name='nombre_usuario',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
