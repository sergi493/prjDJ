# Generated by Django 5.0.3 on 2024-08-19 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0068_avui_marge_avui_targeta_avui_total_alter_avui_calaix_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(upload_to='imagenes/'),
        ),
    ]
