from django.db import models


class UnsafeUser(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password_hash = models.BinaryField()
    description = models.CharField(max_length=1024, default="")
    
    def __str__(self):
        return self.username

