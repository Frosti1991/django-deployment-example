from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)

    #additional than User Class
    portfolio_site=models.URLField(blank=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True) #subdirectory in the media folder

    def __str__(self):
        return self.user.username