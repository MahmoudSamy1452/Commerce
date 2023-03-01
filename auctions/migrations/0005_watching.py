# Generated by Django 4.1.6 on 2023-02-07 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comment_user_listing_closed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched', to='auctions.listing')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Watcher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
