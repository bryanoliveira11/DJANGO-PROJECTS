# Generated by Django 5.0.6 on 2024-07-23 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0013_genres_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
