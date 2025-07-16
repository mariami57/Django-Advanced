from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=20)
    pages = models.PositiveIntegerField()
    description = models.TextField(max_length=100)
    authors = models.ManyToManyField(to='Author', related_name='books')

class Author(models.Model):
    name = models.CharField(max_length=30)

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    established_year = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

class Review(models.Model):
    description = models.TextField()
    book = models.ForeignKey(to='Book', related_name='reviews', on_delete=models.CASCADE)