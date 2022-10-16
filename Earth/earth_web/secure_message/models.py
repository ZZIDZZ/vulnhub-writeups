from django.db import models

# Create your models here.
class EncryptedMessage(models.Model):
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.message
