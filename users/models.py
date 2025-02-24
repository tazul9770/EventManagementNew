from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images', blank=True, default='profile_images/default.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
