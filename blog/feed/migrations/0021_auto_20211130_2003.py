# Generated by Django 3.2.8 on 2021-11-30 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0020_alter_post_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='imagen',
            field=models.ImageField(default='feed/static/images/default.jpg', upload_to='feed/static'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tipo_17_ODS',
            field=models.CharField(choices=[('Fin de la pobreza', 1), (2, 'Hambre cero'), (3, 'Salud y bienestar'), (4, 'Educación de calidad'), (5, 'Igualdad de género'), (6, 'Agua limpia y saneamiento'), (7, 'Energía asequible y no contaminante'), (8, 'Trabajo y crecimiento económico'), (9, 'Industria, innovación e infraestructura'), (10, 'Reducción de las desigualdades'), (11, 'Ciudades y comunidades sostenibles'), (12, 'Producción y consumo responsables'), (13, 'Acción por el clima'), (14, 'Vida submarina'), (15, 'Vida de ecosistemas terrestres'), (16, 'Paz y justicia para todos'), (17, 'Alianzas para lograr los objetivos')], default=1, max_length=50),
        ),
    ]
