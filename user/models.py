from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    full_name = models.CharField(max_length=150)


class EmployeeUser(BaseUser):
    pass


class EmployerUser(BaseUser):
    pass
