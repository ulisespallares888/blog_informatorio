# Generated by Django 3.2.8 on 2021-11-30 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0022_alter_post_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='imagen',
            field=models.ImageField(default='feed/static/images/default.jpg', upload_to='imagenes_posts'),
        ),
    ]
