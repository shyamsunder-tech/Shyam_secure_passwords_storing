from django.db import models
from django.contrib.auth.models import User

class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length=100,default='dinesh')
    password = models.CharField(max_length=200,default='[assword]')
    email = models.CharField(max_length=200,default='dinesh@gmail.com')
    logo = models.CharField(max_length=300,default='logo')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
    