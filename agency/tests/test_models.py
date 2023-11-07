from django.contrib.auth import get_user_model
from django.test import TestCase

from agency.models import Newspaper, Topic


class ModelTests(TestCase):
    def test_newspaper_str(self):
        redactor = get_user_model().objects.create_user(
            username="amer", password="12345"
        )
        topic = Topic.objects.create(name="Test Topic")
        newspaper = Newspaper.objects.create(
            title="Test Title",
            content="Test Content",
            topic=topic,
        )
        newspaper.publishers.add(redactor)

        self.assertEqual(str(newspaper), newspaper.title)

    def test_redactor_str(self):
        redactor = get_user_model().objects.create_user(
            first_name="Test First Name",
            last_name="Test Last Name",
            username="amer",
            password="12345",
            years_of_experience=5,
        )

        self.assertEqual(
            str(redactor), f"{redactor.first_name} {redactor.last_name}"
        )

    def test_topic_str(self):
        topic = Topic.objects.create(name="Test Topic")

        self.assertEqual(str(topic), topic.name)
