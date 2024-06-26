# Generated by Django 5.0.4 on 2024-05-25 20:03

import cloudinary.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('username', models.CharField(max_length=75, null=True, unique=True)),
                ('phone_number', models.CharField(max_length=75, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('password', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='ImageData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', cloudinary.models.CloudinaryField(max_length=255, validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'gif'])], verbose_name='images')),
                ('caption', models.CharField(max_length=40)),
                ('image_date_time', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_images', to='instagram.userinfomodel')),
            ],
        ),
        migrations.CreateModel(
            name='DummyImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', cloudinary.models.CloudinaryField(max_length=255, verbose_name='dimage')),
                ('caption', models.CharField(max_length=40)),
                ('image_date_time', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_dummy_images', to='instagram.userinfomodel')),
            ],
        ),
    ]
