# Generated by Django 5.0.3 on 2024-05-06 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_alter_ticket_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='comp_banc',
            field=models.CharField(default=' ', max_length=200),
        ),
    ]
