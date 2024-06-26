# Generated by Django 5.0.6 on 2024-06-19 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('steam_appid', models.CharField(max_length=150)),
                ('short_description', models.CharField(max_length=500)),
                ('header_image', models.ImageField(blank=True, default='', upload_to='games/headers/%Y/%m/%d/')),
                ('minimum_requirements', models.TextField()),
                ('recommended_requirements', models.TextField()),
                ('developers', models.CharField(max_length=150)),
                ('publishers', models.CharField(max_length=150)),
                ('price', models.CharField(max_length=50)),
                ('screenshot1', models.ImageField(blank=True, default='', upload_to='games/screenshots/%Y/%m/%d/')),
                ('screenshot2', models.ImageField(blank=True, default='', upload_to='games/screenshots/%Y/%m/%d/')),
                ('screenshot3', models.ImageField(blank=True, default='', upload_to='games/screenshots/%Y/%m/%d/')),
                ('screenshot4', models.ImageField(blank=True, default='', upload_to='games/screenshots/%Y/%m/%d/')),
                ('background_raw', models.ImageField(blank=True, default='', upload_to='games/backgrounds/%Y/%m/%d/')),
            ],
        ),
    ]
