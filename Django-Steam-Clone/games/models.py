from django.db import models


class Games(models.Model):
    name = models.CharField(max_length=200)
    steam_appid = models.CharField(max_length=150)
    short_description = models.CharField(max_length=500)
    header_image = models.ImageField(
        upload_to='games/headers/%Y/%m/%d/',
        blank=True,
        default='',
    )
    minimum_requirements = models.TextField(null=True, blank=True)
    recommended_requirements = models.TextField(null=True, blank=True)
    developers = models.CharField(max_length=150)
    publishers = models.CharField(max_length=150)
    price = models.CharField(max_length=50, null=True, blank=True)
    screenshot1 = models.ImageField(
        upload_to='games/screenshots/%Y/%m/%d/',
        blank=True,
        default='',
    )
    screenshot2 = models.ImageField(
        upload_to='games/screenshots/%Y/%m/%d/',
        blank=True,
        default='',
    )
    screenshot3 = models.ImageField(
        upload_to='games/screenshots/%Y/%m/%d/',
        blank=True,
        default='',
    )
    screenshot4 = models.ImageField(
        upload_to='games/screenshots/%Y/%m/%d/',
        blank=True,
        default='',
    )
    background_raw = models.ImageField(
        upload_to='games/backgrounds/%Y/%m/%d/',
        blank=True,
        default='',
    )
