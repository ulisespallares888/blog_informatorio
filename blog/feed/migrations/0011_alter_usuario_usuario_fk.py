# Generated by Django 3.2.8 on 2021-11-29 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0010_post_actualizado_en'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='usuario_fk',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]