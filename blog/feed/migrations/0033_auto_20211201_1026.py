# Generated by Django 3.2.8 on 2021-12-01 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0032_alter_post_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='imagen',
            field=models.FileField(default='ost_default.jpg', upload_to='imagenes_posts'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='foto',
            field=models.FileField(default='foto_default.png', upload_to='fotos_perfil'),
        ),
    ]
