# Generated by Django 4.2.17 on 2024-12-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_santa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='budget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]