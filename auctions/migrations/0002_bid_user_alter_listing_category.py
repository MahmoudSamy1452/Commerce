# Generated by Django 4.1.6 on 2023-02-05 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='User',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.TextField(choices=[('Electronics', 'Electronics'), ('Toys', 'Toys'), ('Fashion', 'Fashion'), ('Home', 'Home'), ('Other', 'Other')]),
        ),
    ]
