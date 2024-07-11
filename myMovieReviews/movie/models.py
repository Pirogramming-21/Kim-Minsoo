from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.CharField(max_length=10)
    director = models.CharField(max_length=50)
    stars = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    runningtime = models.CharField(max_length=15)
    content = models.TextField()