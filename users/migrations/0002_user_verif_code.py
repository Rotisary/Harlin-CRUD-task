# Generated by Django 5.1.3 on 2024-11-07 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verif_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
