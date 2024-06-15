from django.db import models
from django.contrib.auth import get_user_model
import uuid


# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.jpg')

