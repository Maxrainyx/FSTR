
from django.db import models


class User(models.Model):
    """ Model representing a user. """
    name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    otc = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    email = models.EmailField(unique=True)

    class Meta:
        """ Used for a custom table name. """
        db_table = 'pass_user'


class Pass(models.Model):
    """ Model for storing new passes """
    ADDED_STATUS = [
        ('new', 'новое'),
        ('pending', 'взято в работу'),
        ('accepted', 'успешно'),
        ('rejected', 'не принято'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=255, blank=True)
    add_time = models.DateTimeField()
    coordinates = models.ForeignKey('Coordinates', on_delete=models.CASCADE)
    levels = models.ForeignKey('Level', blank=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=8, choices=ADDED_STATUS, default='new')

    class Meta:
        """ Used for a custom table name. """
        db_table = 'pass_pass'


class Coordinates(models.Model):
    """ Model for storing coordinates of the passes """
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    class Meta:
        """ Used for a custom table name. """
        db_table = 'pass_coordinates'


class Level(models.Model):
    """ Model for storing difficulty levels of the passes """
    winter_level = models.CharField(max_length=3, blank=True)
    summer_level = models.CharField(max_length=3, blank=True)
    autumn_level = models.CharField(max_length=3, blank=True)
    spring_level = models.CharField(max_length=3, blank=True)

    class Meta:
        """ Used for a custom table name. """
        db_table = 'pass_level'


class Images(models.Model):
    """ Model for storing images of the passes """
    passes = models.ForeignKey(Pass, related_name='images', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=20)
    data = models.BinaryField()

    class Meta:
        """ Used for a custom table name. """
        db_table = 'pass_images'
