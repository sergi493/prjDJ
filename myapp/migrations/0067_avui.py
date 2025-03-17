# Generated by Django 5.0.3 on 2024-08-02 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0066_alter_ticket_metodo_pago'),
    ]

    operations = [
        migrations.CreateModel(
            name='avui',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('calaix', models.DecimalField(decimal_places=2, max_digits=9999999)),
                ('ingressat_banc', models.DecimalField(decimal_places=2, max_digits=9999999)),
            ],
        ),
    ]
