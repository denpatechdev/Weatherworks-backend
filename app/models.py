from django.db import models

class Comment(models.Model):
    area = models.CharField(max_length=256)
    pinned = models.BooleanField(default=False)
    contents = models.CharField(max_length=500)