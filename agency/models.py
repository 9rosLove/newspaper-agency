from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from newspaper_agency import settings


class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("agency:redactor-newspapers", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(
        to=Topic, on_delete=models.CASCADE, related_name="newspapers"
    )
    publishers = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="newspapers"
    )

    @property
    def get_short_content(self):
        return (
            self.content[:150] + "..."
            if len(self.content) > 150
            else self.content
        )

    @property
    def get_short_publishers(self):
        publishers = self.publishers.all()
        short_list = ", ".join(
            f"<a href='{publisher.get_absolute_url()}'>{publisher}</a>"
            for publisher in publishers
        )
        if len(publishers) > 2:
            short_list += "..."
        return short_list

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-publication_date"]
