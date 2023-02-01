from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.urls import reverse


class PerevalAdded(models.Model):
    """" # """
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    raw_data = JSONField()
    images = JSONField()
    bTitle = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    other_title = models.CharField(max_length=100)
    connect = models.CharField(max_length=100)
    coord_id = models.ForeignKey('Coords', on_delete=models.CASCADE, related_name='coord_id')
    spring = models.CharField(max_length=100)
    summer = models.CharField(max_length=100)
    autumn = models.CharField(max_length=100)
    winter = models.CharField(max_length=100)


class PerevalAreas(models.Model):
    """" # """
    id_parent = ...
    title = models.TextField(max_length=100)


class Activities(models.Model):
    ...

unique = True


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def __str__(self):
        return f'lat: {self.latitude}, lon: {self.longitude}, h: {self.height}'


class Post(models.Model):
    """ Post model with 'title', 'text' fields """
    title = models.CharField(max_length=255)  # title column
    text = RichTextUploadingField()  # text column
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_category')  # o-t-o - Category
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')  # o-t-o with User

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        """ Method for the redirection """
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    """ Comment model with 'text' fields and One-To-One relationship with the Post model """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    text = models.TextField(max_length=255)  # simple text field to contain the comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')  # o-t-o with Post
    rating = models.IntegerField(default=0)  # rating of the comment, starts from 0 initially
    created = models.DateTimeField(auto_now_add=True)  # time-field with automatically managed creation time
    approved = models.BooleanField(default=False)  # to check whether comment approved by the post author or not

    def __str__(self):
        return f'{self.text}'

    def get_absolute_url(self):
        """ Method for the redirection """
        return reverse('post_detail', args=[str(self.post_id)])
