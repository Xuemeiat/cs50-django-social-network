from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True
    )

    def __str__(self):
        return f"{self.user} posted at {self.timestamp}"

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    followers = models.ManyToManyField(
        User,
        related_name="following",
        blank=True)

    def __str__(self):
        return self.user.username  
