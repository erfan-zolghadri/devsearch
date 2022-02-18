from django.db import models
from uuid import uuid4

from uuid import uuid4
from users.models import Profile


class Tag(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,
                          unique=True, editable=False)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,
                          unique=True, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='projects', null=True, blank=True)
    source_link = models.CharField(max_length=500, null=True, blank=True)
    demo_link = models.CharField(max_length=500, null=True, blank=True)
    votes = models.IntegerField(default=0)
    votes_ratio = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def reviewers(self):
        return self.review_set.all().values_list('profile__id', flat=True)

    @property
    def update_votes(self):
        reviews_count = self.review_set.all().count()
        up_votes_count = self.review_set.filter(vote='Up').count()

        self.votes = reviews_count
        self.votes_ratio = (up_votes_count / reviews_count) * 100
        self.save()


class Review(models.Model):
    VOTE_CHOICES = (
        ('Up', 'Up Vote'),
        ('Down', 'Down Vote')
    )

    id = models.UUIDField(default=uuid4, primary_key=True,
                          unique=True, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vote = models.CharField(
        max_length=10, choices=VOTE_CHOICES, default='Up Vote')
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ['profile', 'project'],
        ]

    def __str__(self):
        return str(self.vote)
