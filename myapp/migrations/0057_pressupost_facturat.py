# Generated by Django 5.0.3 on 2024-07-29 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0056_producto_marge_producto_preu_distribuidor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pressupost',
            name='facturat',
            field=models.CharField(default='no', max_length=100),
        ),
    ]
