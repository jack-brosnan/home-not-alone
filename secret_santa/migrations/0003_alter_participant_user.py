# Generated by Django 4.2.17 on 2024-12-17 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('secret_santa', '0002_alter_event_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
