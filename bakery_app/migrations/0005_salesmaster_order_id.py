# Generated by Django 5.0.1 on 2024-02-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery_app', '0004_alter_salesmaster_item_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesmaster',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]