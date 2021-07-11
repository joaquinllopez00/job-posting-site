from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# User model @ line 13
# Listing model @ line 35
# Category model @ line 42
# Notifications model @ line 65
# Applicant model @ line 71
# FavoriteJob model @ line 80


class User(AbstractUser):
    classification = (('employer', 'Employer'), ('employee', 'Employee'))
    name = models.CharField(max_length=150)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(choices=classification,
                            default=False, max_length=10)

    def __str__(self):
        return self.name + self.email


JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(User, related_name='User',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    category = models.ForeignKey(
        Category, related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300)
    company_description = models.CharField(
        max_length=250, blank=True, null=True)
    url = models.URLField(max_length=200)
    post_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Notification(models.Model):
    mentioned = models.ForeignKey(User, on_delete=models.CASCADE)
    mention_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    mark_as_read = models.BooleanField(default=False)


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Listing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.title


class FavoriteJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Listing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.title
