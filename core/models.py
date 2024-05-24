from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Activity(models.Model):
    TYPE_CHOICES = [
        ("positive", "Positive"),
        ("negative", "Negative"),
        ("neutral", "Neutral"),
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    public = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    date_added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default="neutral",
    )

    def __str__(self):
        return self.title


class ActivityInstance(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    # might need to change start_time and date_time logic, we'll see
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField()

    def __str__(self):
        return self.activity + " instance"
