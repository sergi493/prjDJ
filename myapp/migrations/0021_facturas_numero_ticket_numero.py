# Generated by Django 5.0.3 on 2024-04-04 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_rename_factura_productoenfactura_factura_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturas',
            name='numero',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='ticket',
            name='numero',
            field=models.IntegerField(default=1),
        ),
    ]
