# Generated by Django 5.1.6 on 2025-03-05 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_profile_recommended_by_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='code',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
