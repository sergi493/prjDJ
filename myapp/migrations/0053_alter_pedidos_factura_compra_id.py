# Generated by Django 5.0.3 on 2024-07-10 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0052_pedidos_factura_compra_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidos',
            name='factura_compra_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.facturacompra'),
        ),
    ]
