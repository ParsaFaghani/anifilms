# Generated by Django 4.2.14 on 2024-08-05 14:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anim', '0009_alter_anim_sub_accepted_alter_anim_sub_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anim',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='accepted'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='max_episod',
            field=models.IntegerField(default=12, verbose_name='max_episod'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='name_Japanese',
            field=models.CharField(max_length=255, unique=True, verbose_name='name_Japanese'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='name_english',
            field=models.CharField(max_length=255, unique=True, verbose_name='name_english'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='name_farsi',
            field=models.CharField(max_length=255, unique=True, verbose_name='name_farsi'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='photo',
            field=models.ImageField(default='media/photo/default.jpg', upload_to='', verbose_name='photo'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='publication_year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2024)], verbose_name='publication_year'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='seasion',
            field=models.IntegerField(default=1, verbose_name='seasion'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='status',
            field=models.CharField(choices=[('منتشر نشده', 'منتشر نشده'), ('در حال انتشار', 'در حال انتشار'), ('منتشر شده', 'منتشر شده')], max_length=13, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='anim',
            name='trailer',
            field=models.FileField(blank=True, upload_to='media/TR/', verbose_name='trailer'),
        ),
    ]
