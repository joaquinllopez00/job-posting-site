from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    classification = (('employer', 'Employer'), ('employee', 'Employee'))
    name = models.CharField(max_length=150)
    bio = models.TextField(null=True, blank=True)
    signed_up = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(choices=classification,
                            default=False, max_length=10)
    # Uncomment & fill in model arg when ready
    # watch_list = models.ManyToManyField(JOB_POST, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name + self.email
