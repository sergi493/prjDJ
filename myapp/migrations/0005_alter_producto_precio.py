# Generated by Django 5.0.2 on 2024-03-18 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_facturas_persona_producto_ticket_remove_task_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=9999999),
        ),
    ]
