# Generated by Django 5.0.2 on 2024-07-03 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_alter_facturas_abono_alter_ticket_abono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoenticket',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
