# Generated by Django 5.0.1 on 2024-02-03 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery_app', '0006_salesmaster_created_dt_salesmaster_order_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_dt', models.DateField(blank=True, null=True)),
                ('element', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.CharField(blank=True, max_length=100, null=True)),
                ('unit_price', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.CharField(blank=True, max_length=100, null=True)),
                ('unit_of_measurement', models.CharField(blank=True, choices=[('Kilogram', 'Kilogram'), ('Gram', 'Gram'), ('Milligram', 'Milligram'), ('Liter', 'Liter'), ('Milliliter', 'Milliliter')], max_length=100, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_dt', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
