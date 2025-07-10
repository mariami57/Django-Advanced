
from django.db import models

from photos.models import Photo


# Create your models here.
class Comment(models.Model):
    comment_text = models.TextField(max_length=300)
    date_and_time_of_publication = models.DateTimeField(auto_now_add=True)
    to_photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text[:20]

    class Meta:
        ordering = ['-date_and_time_of_publication']


class Like(models.Model):
    to_photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE)