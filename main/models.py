import datetime
from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    detail = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField(default=datetime.time(7, 0, 0))
    end_time = models.TimeField(default=datetime.time(7, 0, 0))
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    