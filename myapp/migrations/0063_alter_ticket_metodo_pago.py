# Generated by Django 5.0.3 on 2024-08-01 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0062_rename_pressupost_producteenreparacio_reparacio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='metodo_pago',
            field=models.CharField(choices=[('Efectiu', 'Efectiu'), ('Targeta', 'Tarjeta'), ('Transferencia', 'Transferencia'), ('Chec bancari', 'Chec bancari'), ('domiciliacio', 'domiciliacio')], default='Efectivo', max_length=20),
        ),
    ]
