# Generated by Django 5.1.3 on 2024-11-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_episodes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]