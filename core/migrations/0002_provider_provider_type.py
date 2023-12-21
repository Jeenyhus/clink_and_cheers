# Generated by Django 5.0 on 2023-12-21 05:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='provider_type',
            field=models.CharField(choices=[('Bartender', 'Bartender'), ('Chef', 'Chef')], default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]