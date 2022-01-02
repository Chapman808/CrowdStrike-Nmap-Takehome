from django.db import models

class NmapResult(models.Model):
    host =  models.TextField()
    content = models.TextField()
    def __str__(self):
        return self.content