# Generated by Django 3.2.8 on 2021-11-29 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_alter_usuario_usuario_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='comentador',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='feed.usuario'),
        ),
    ]
