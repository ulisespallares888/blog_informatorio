# Generated by Django 3.2.8 on 2021-12-02 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0037_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipo_usuario',
            name='descripcion',
        ),
    ]
