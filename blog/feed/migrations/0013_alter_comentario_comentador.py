# Generated by Django 3.2.8 on 2021-11-29 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0012_alter_comentario_comentador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='comentador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feed.usuario'),
        ),
    ]
