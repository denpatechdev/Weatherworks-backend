from django.db import models

class Comment(models.Model):
    ip = models.GenericIPAddressField()
    area = models.CharField(max_length=256)
    contents = models.CharField(max_length=500)

class Like(models.Model):
    ip = models.GenericIPAddressField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)