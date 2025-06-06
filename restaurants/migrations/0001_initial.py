# Generated by Django 4.2.20 on 2025-05-09 08:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('open_hours', models.TextField(blank=True, null=True)),
                ('google_rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('place_id', models.CharField(max_length=100, unique=True)),
                ('img_url', models.URLField(blank=True, max_length=255, null=True)),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
                ('website', models.URLField(blank=True, max_length=255, null=True)),
                ('user_ratings_total', models.IntegerField(blank=True, null=True)),
                ('google_photo_reference', models.TextField(blank=True, null=True)),
                ('types', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('img_url', models.URLField(blank=True, max_length=255, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='restaurants.restaurant')),
            ],
        ),
    ]
