from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.
class Activity(models.Model):
    TYPE_CHOICES = [
        ("positive", "Positive"),
        ("negative", "Negative"),
        ("neutral", "Neutral"),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    favorite = models.BooleanField(default=False)
    description = models.CharField(max_length=300, blank=True, default="")
    date_added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default="neutral",
    )

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("activity_statistics", kwargs={"pk": self.pk})


class ActivityInstance(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    # might need to change start_time and date_time logic, we'll see
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.activity.title + " instance"
