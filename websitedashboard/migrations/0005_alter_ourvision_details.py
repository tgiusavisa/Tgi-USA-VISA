# Generated by Django 5.1.2 on 2025-06-01 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websitedashboard', '0004_details_aboutus_details_ourgoals_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ourvision',
            name='details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Our_vision', to='websitedashboard.details'),
        ),
    ]
