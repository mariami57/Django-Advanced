from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=15)


class Todo(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    state = models.BooleanField(default=False)