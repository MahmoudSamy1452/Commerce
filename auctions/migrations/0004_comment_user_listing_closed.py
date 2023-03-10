# Generated by Django 4.1.6 on 2023-02-06 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='User',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commentor', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
