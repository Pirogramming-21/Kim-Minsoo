from django.db import models

class DevTool(models.Model):
    name = models.CharField(max_length=200, unique=True)
    kind = models.CharField(max_length=50)   
    content = models.TextField()            

    def __str__(self):
        return self.name
