from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django_summernote.widgets import SummernoteWidget

from agency.models import Newspaper, Redactor


class SearchFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FieldWithButtons(
                f"{self.obj}",
                StrictButton("Search", type="submit"),
                input_size="input-group-sm",
            )
        )


class RedactorRegistrationForm(UserCreationForm):
    class Meta:
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )


class RedactorForm(UserCreationForm):
    class Meta:
        model = Redactor
        fields = [
            "first_name",
            "last_name",
            "years_of_experience",
            "username",
            "password1",
            "password2",
            "avatar",
        ]


class NewspaperForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget)
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class TopicSearchForm(SearchFormMixin, forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )
    obj = "name"


class NewspaperSearchForm(SearchFormMixin, forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
    )
    obj = "title"


class RedactorSearchForm(SearchFormMixin, forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )
    obj = "username"
