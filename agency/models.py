from django.contrib.auth.models import AbstractUser
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateField()
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE, related_name="newspapers")
    publishers = models.ManyToManyField(to=Redactor, related_name="newspapers")

    def __str__(self):
        return self.title
