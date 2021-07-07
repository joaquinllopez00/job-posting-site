from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    full_name = models.CharField(max_length=150)
    bio = models.TextField(null=True, blank=True)
    signed_up = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    is_employer = models.BooleanField(default=False)
    # Uncomment & fill in model arg when ready
    # watch_list = models.ManyToManyField(JOB_POST, null=True, blank=True)

    def __str__(self):
        return self.email
