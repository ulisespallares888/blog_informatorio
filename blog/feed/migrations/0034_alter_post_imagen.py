# Generated by Django 3.2.8 on 2021-12-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0033_auto_20211201_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='imagen',
            field=models.FileField(default='post_default.jpg', upload_to='imagenes_posts'),
        ),
    ]
