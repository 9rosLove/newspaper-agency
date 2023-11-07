from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from agency.models import Topic, Newspaper


class PublicAccessTests(TestCase):
    def setUp(self) -> None:
        self.topic = Topic.objects.create(name="Test Topic")
        self.redactor1 = get_user_model().objects.create_user(
            first_name="Peter",
            last_name="Hansen",
            username="hansenpeter",
            password="Password12343***",
            years_of_experience=5,
        )
        self.redactor2 = get_user_model().objects.create_user(
            first_name="Bob",
            last_name="Smith",
            username="bob",
            password="FJFDfsdj12345***",
            years_of_experience=5,
        )
        self.newspaper = Newspaper.objects.create(
            title="Test Title",
            content="Test Content",
            topic=self.topic,
        )
        self.newspaper.publishers.set([self.redactor1, self.redactor2])

    def test_login_required_create_newspaper(self):
        response = self.client.get(reverse("agency:newspaper-create"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_update_newspaper(self):
        response = self.client.get(
            reverse(
                "agency:newspaper-update", kwargs={"pk": self.newspaper.pk}
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_login_required_delete_newspaper(self):
        response = self.client.get(
            reverse(
                "agency:newspaper-delete", kwargs={"pk": self.newspaper.pk}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_redactor_register(self):
        response = self.client.get(reverse("agency:register"))

        self.assertEqual(response.status_code, 200)

    def test_login_required_redactor_update(self):
        response = self.client.get(
            reverse("agency:redactor-update", kwargs={"pk": self.redactor1.pk})
        )

        self.assertEqual(response.status_code, 302)

    def test_login_required_redactor_delete(self):
        response = self.client.get(
            reverse("agency:redactor-delete", kwargs={"pk": self.redactor1.pk})
        )

        self.assertEqual(response.status_code, 302)

    def test_login_required_topic_create(self):
        response = self.client.get(reverse("agency:topic-create"))

        self.assertEqual(response.status_code, 302)


class SearchFunctionalityTests(TestCase):
    def setUp(self):
        self.topic1 = Topic.objects.create(name="FoodTopic")
        self.topic2 = Topic.objects.create(name="SportsTopic")
        self.redactor1 = get_user_model().objects.create_user(
            first_name="Fred",
            last_name="Gertrude",
            username="redactortest",
            password="FFDhfdgsgdr1422412***",
            years_of_experience=2,
        )
        self.redactor2 = get_user_model().objects.create_user(
            first_name="Fab",
            last_name="Gabriel",
            username="redactortest2",
            password="FFDhfdgsgdr1422412***",
            years_of_experience=3,
        )

        self.newspaper1 = Newspaper.objects.create(
            title="Food",
            content="Food is good",
            topic=self.topic1,
        )

        self.newspaper2 = Newspaper.objects.create(
            title="Sports",
            content="Lorem ipsum",
            topic=self.topic2,
        )

        self.newspaper1.publishers.set([self.redactor1, self.redactor2])
        self.newspaper2.publishers.add(self.redactor1)

    def test_newspaper_search(self):
        response = self.client.get(reverse("agency:index"), {"title": "Food"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Food")
        self.assertNotContains(response, "Sports")

    def test_redactor_search(self):
        response = self.client.get(
            reverse("agency:redactor-list"), {"username": "redactortest"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "redactortest")
        self.assertNotContains(response, "Food")

    def test_topic_search(self):
        response = self.client.get(
            reverse("agency:topic-list"), {"name": "FoodTopic"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FoodTopic")
        self.assertNotContains(response, "SportsTopic")
