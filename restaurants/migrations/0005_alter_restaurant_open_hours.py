# Generated by Django 4.2.20 on 2025-05-19 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_rename_img_url_restaurant_image_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='open_hours',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
