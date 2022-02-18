from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Profile(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,
                          unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, null=True, blank=True)
    headline = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profiles', null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    github = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,
                          unique=True, editable=False)
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='messages')
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Skill(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,
                          unique=True, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name