from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid


# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.jpg')


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='tasks_created', on_delete=models.CASCADE)
    assigned_to = models.EmailField()
    status = models.CharField(max_length=10, default='pending')  # completed or pending
    priority = models.CharField(max_length=10, default="high")

    due_date = models.DateField(default=timezone.now().date())
    completed_date = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.task_name

