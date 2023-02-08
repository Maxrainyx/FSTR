from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.IntegerField()


STATUS = [
    ('new', 'новое'),
    ('pending', 'взято в работу'),
    ('accepted', 'успешно'),
    ('rejected', 'не принято'),
]


class Pass(models.Model):
    """" # TODO """
    date_added = models.DateTimeField(auto_now_add=True)
    bTitle = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    other_title = models.CharField(max_length=100)
    connect = models.CharField(max_length=100)
    coord_id = models.ForeignKey('Coordinates',
                                 on_delete=models.CASCADE,
                                 related_name='coord_id'
                                 )
    spring = models.CharField(max_length=100)
    summer = models.CharField(max_length=100)
    autumn = models.CharField(max_length=100)
    winter = models.CharField(max_length=100)
    pass_images = models.ManyToManyField('PassImages',
                                         through='Images',)
    status = models.CharField(max_length=255,
                              choices=STATUS,
                              default='new',)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Activities(models.Model):
    title = models.CharField(max_length=100)
    pass_added = models.ManyToManyField(Pass)


class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()
    pass_id = models.ForeignKey('Pass', on_delete=models.CASCADE)

    def __str__(self):
        return f'lat: {self.latitude}, lon: {self.longitude}, h: {self.height}'


class PassImages(models.Model):
    time_added = models.DateTimeField(auto_now_add=True)
    img = models.BinaryField(null=True)


class Images(models.Model):
    pass_image = models.ForeignKey(PassImages, on_delete=models.CASCADE)
    pass_added = models.ForeignKey(Pass, on_delete=models.CASCADE)
