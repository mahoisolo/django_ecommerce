# Generated by Django 5.1.2 on 2024-10-22 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='-'),
            preserve_default=False,
        ),
    ]
