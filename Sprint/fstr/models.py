from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.urls import reverse


class PerevalAdded(models.Model):
    """" # TODO """
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    raw_data = JSONField()
    bTitle = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    other_title = models.CharField(max_length=100)
    connect = models.CharField(max_length=100)
    coord_id = models.ForeignKey('Coords', on_delete=models.CASCADE, related_name='coord_id')
    spring = models.CharField(max_length=100)
    summer = models.CharField(max_length=100)
    autumn = models.CharField(max_length=100)
    winter = models.CharField(max_length=100)
    pereval_images = models.ManyToManyField('PerevalImages', through='Images')


class Activities(models.Model):
    title = models.CharField(max_length=100)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def __str__(self):
        return f'lat: {self.latitude}, lon: {self.longitude}, h: {self.height}'


class PerevalImages(models.Model):
    time_added = models.DateTimeField(auto_now_add=True)
    img = models.BinaryField(null=True)


class Images(models.Model):
    pereval_image = models.ManyToManyField(PerevalImages)
    pereval_added = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)

