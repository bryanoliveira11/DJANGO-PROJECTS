from django.db import models


class Genres(models.Model):
    name = models.CharField(max_length=150, unique=True)
    image_url = models.CharField(max_length=150, blank=True, null=True)


class Reviews(models.Model):
    description = models.CharField(max_length=150)
    total_reviews = models.DecimalField(max_digits=20, decimal_places=0)
    total_positive = models.DecimalField(max_digits=20, decimal_places=0)
    total_negative = models.DecimalField(max_digits=20, decimal_places=0)
    positive_percent = models.DecimalField(
        max_digits=3, decimal_places=0, null=True, blank=True
    )


class Games(models.Model):
    name = models.CharField(max_length=200)
    steam_appid = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    is_free = models.BooleanField(default=False)
    short_description = models.CharField(max_length=500)
    sale_image = models.CharField(max_length=500)
    capsule_image = models.ImageField(
        upload_to='games/capsule_images/%Y/%m/%d/',
        blank=True,
        default='',
    )
    minimum_requirements = models.TextField(null=True, blank=True)
    recommended_requirements = models.TextField(null=True, blank=True)
    developers = models.CharField(max_length=150)
    publishers = models.CharField(max_length=150)
    price_initial = models.CharField(max_length=50, null=True, blank=True)
    price_final = models.CharField(max_length=50, null=True, blank=True)
    discount_percent = models.DecimalField(
        max_digits=3, null=True, blank=True, decimal_places=1
    )
    screenshot1 = models.CharField(max_length=500)
    screenshot2 = models.CharField(max_length=500)
    screenshot3 = models.CharField(max_length=500)
    screenshot4 = models.CharField(max_length=500)
    screenshot5 = models.CharField(max_length=500)
    background = models.CharField(max_length=500, null=True, blank=True)
    background_raw = models.CharField(max_length=500)
    movie1 = models.CharField(max_length=500, null=True, blank=True)
    movie2 = models.CharField(max_length=500, null=True, blank=True)
    movie3 = models.CharField(max_length=500, null=True, blank=True)
    genres = models.ManyToManyField(Genres, blank=True, default='')
    reviews = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, null=True, blank=True
    )
