from django.contrib.auth import get_user_model
from django.test import TestCase

from agency.forms import (
    NewspaperSearchForm,
    RedactorSearchForm,
    TopicSearchForm,
    NewspaperForm,
    RedactorForm,
)
from agency.models import Topic


class SearchFormTest(TestCase):
    def test_newspaper_search_form_is_valid(self):
        form_data = {"title": "Test Title"}
        form = NewspaperSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_redactor_search_form_is_valid(self):
        form_data = {"username": "amer"}
        form = RedactorSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_topic_search_form_is_valid(self):
        form_data = {"name": "Test Topic"}
        form = TopicSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class FormTests(TestCase):
    def test_newspaper_form_is_valid(self):
        redactor = get_user_model().objects.create_user(
            username="amer", password="12345"
        )
        topic = Topic.objects.create(name="Test Topic")
        form_data = {
            "title": "Test Title",
            "content": "Test Content",
            "topic": topic,
            "publishers": [
                redactor,
            ],
            "image": None,
        }
        form = NewspaperForm(form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        cleaned_data = form.cleaned_data
        cleaned_data["publishers"] = list(cleaned_data["publishers"])
        self.assertEqual(cleaned_data, form_data)

    def test_redactor_form_is_valid(self):
        form_data = {
            "first_name": "Test First Name",
            "last_name": "Test Last Name",
            "years_of_experience": 5,
            "username": "amer",
            "password1": "QWE123***",
            "password2": "QWE123***",
            "avatar": None,
        }
        form = RedactorForm(form_data)
        print(form.errors)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_topic_form_is_valid(self):
        form_data = {"name": "Test Topic"}
        form = TopicSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
