from django.db import models


class UnsafeUser(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    password_hash = models.BinaryField()
    
    def __str__(self):
        return self.username

