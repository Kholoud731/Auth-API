from django.db import models

class CommonData(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    poster_image = models.ImageField(upload_to='photo/%y/%m/%d', null=True, blank=True)
    casts = models.ManyToManyField('Cast')
    Categories = models.ManyToManyField('Category')

class Cast(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Category(models.Model):
    category = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.category

class Movie(CommonData):
    running_time = models.IntegerField()

class Series(CommonData):
    eps_number = models.IntegerField()

