from django.db import models

# Create your models here.
class MessageTemplate(models.Model):
    name = models.CharField(max_length = 50)
    message = models.CharField(max_length = 2000)
    
    def __str__(self) -> str:
        return self.name