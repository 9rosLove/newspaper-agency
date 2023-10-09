from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from newspaper_agency import settings
import re


class Topic(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="topics/", null=True, blank=True)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to="redactors/", null=True, blank=True)

    def get_absolute_url(self):
        return reverse("agency:redactor-newspapers", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.get_full_name()}"


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
    image = models.ImageField(upload_to="newspapers/", null=True, blank=True)

    @property
    def get_short_content(self):
        short_content = re.sub(r"<[^>]*>", "", self.content)[:150]
        return (
            short_content + "..."
            if len(self.content) > 150
            else self.content
        )

    @property
    def get_short_publishers(self):
        publishers = self.publishers.all()
        short_list = ", ".join(
            f"<a href='{publisher.get_absolute_url()}'>{publisher}</a>"
            for publisher in publishers[:2]
        )
        if len(publishers) > 2:
            short_list += "..."
        return short_list

    @property
    def get_full_publishers(self):
        return ", ".join(
            f"<a href='{publisher.get_absolute_url()}'>{publisher}</a>"
            for publisher in self.publishers.all()
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-publication_date"]
