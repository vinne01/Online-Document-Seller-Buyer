# Generated by Django 5.1 on 2025-01-05 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0006_alter_tweet_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=1.0, max_digits=10),
        ),
    ]
