# Generated by Django 5.0.3 on 2024-07-10 09:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0044_alter_pedidos_factura_compra'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='factura_compra_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='myapp.facturacompra'),
        ),
    ]
