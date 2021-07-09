from django.db import models
from django.utils import timezone



# Create your models here.
class Listing(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey("user.User", on_delete=models.CASCADE)
    applicants = models.ManyToManyField("user.User", symmetrical=False, related_name="applicants")
    def __str__(self):
        return self.title