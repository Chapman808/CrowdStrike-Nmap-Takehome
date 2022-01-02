from django.db import models

class NmapResult(models.Model):
    content = models.TextField()