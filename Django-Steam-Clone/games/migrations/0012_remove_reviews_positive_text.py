# Generated by Django 5.0.6 on 2024-07-12 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0011_reviews_positive_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='positive_text',
        ),
    ]
