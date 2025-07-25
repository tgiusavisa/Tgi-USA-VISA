# Generated by Django 5.1.2 on 2025-06-17 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0003_alter_bookingdetail_appointment_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_proof', models.FileField(upload_to='payment_proofs/')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('under_process', 'Under Process'), ('payment_received', 'Payment Received')], default='under_process', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
