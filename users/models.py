from django.db import models
from django.utils import timezone


class UnsafeUser(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password_hash = models.BinaryField()
    description = models.CharField(max_length=1024, default="")
    
    def __str__(self):
        return self.username


class UserAudit(models.Model):
    user_id = models.ForeignKey(UnsafeUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user_id
