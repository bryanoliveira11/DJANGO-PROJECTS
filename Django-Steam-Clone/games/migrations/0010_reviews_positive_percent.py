# Generated by Django 5.0.6 on 2024-07-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_alter_reviews_total_negative_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='positive_percent',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True),
        ),
    ]
