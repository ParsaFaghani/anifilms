# Generated by Django 4.2.13 on 2024-06-30 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_discountcode_id_alter_follow_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bloger',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='manager',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='translator',
            field=models.BooleanField(default=False),
        ),
    ]
