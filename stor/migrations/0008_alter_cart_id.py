# Generated by Django 5.1.3 on 2024-11-15 05:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stor', '0007_alter_orderitem_product_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6d46d24f-327c-4eb9-8cf5-6e8011ea0ed9'), primary_key=True, serialize=False),
        ),
    ]
