# Generated by Django 5.0.3 on 2024-07-10 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0041_pedidos'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='rebut',
            field=models.CharField(default='NO', max_length=10),
        ),
    ]
