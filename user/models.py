from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from user.managers import CustomUserManager


JOB_TYPE = (
    ('M', "Male"),
    ('F', "Female"),
)

CLASSIFICATION = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    classification = models.CharField(default="employee", choices=CLASSIFICATION,  max_length=10)
    gender = models.CharField(default="M", choices=JOB_TYPE, max_length=1)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name+ ' ' + self.last_name
    objects = CustomUserManager()
