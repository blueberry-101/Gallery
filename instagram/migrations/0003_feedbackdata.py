# Generated by Django 5.0.4 on 2024-05-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_alter_dummyimages_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_changing_feature', models.TextField(verbose_name='Game-changing Feature')),
                ('contributor', models.CharField(blank=True, max_length=255, verbose_name='Contributor')),
                ('like_most', models.TextField(verbose_name='Like Most')),
                ('flaw', models.TextField(blank=True, verbose_name='Flaw')),
            ],
        ),
    ]