from django.db import models

class NmapResult(models.Model):
    host =  models.TextField()
    ports = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.ports
