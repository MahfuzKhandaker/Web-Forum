from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=50)
    profile_pic = models.ImageField(default='avatar.svg', upload_to='profile_pics')
    bio = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f"{self.user.username}"
