# Generated by Django 3.1 on 2024-06-18 04:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anim', '0006_auto_20240614_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='anim',
            name='publication_year',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2024)]),
            preserve_default=False,
        ),
    ]
