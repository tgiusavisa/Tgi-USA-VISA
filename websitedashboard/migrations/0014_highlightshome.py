# Generated by Django 5.1.2 on 2025-06-05 05:28

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websitedashboard', '0013_faqshome'),
    ]

    operations = [
        migrations.CreateModel(
            name='highlightshome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=200)),
                ('description', tinymce.models.HTMLField()),
            ],
            options={
                'verbose_name_plural': 'Highlights',
            },
        ),
    ]
