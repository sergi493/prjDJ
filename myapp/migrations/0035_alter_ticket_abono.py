# Generated by Django 5.0.2 on 2024-07-03 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0034_alter_productoenticket_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='abono',
            field=models.IntegerField(null=True),
        ),
    ]
