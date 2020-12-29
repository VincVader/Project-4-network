from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ID: {self.pk} Author: {self.author} Posted at: {self.date_posted}."