from django import forms
from django.contrib.auth import get_user_model

from agency.models import Newspaper


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Newspaper
        fields = '__all__'
