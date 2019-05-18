from django import forms
from django.forms import ModelForm

from account.models import Account


def AccountForm(ModelForm):
    class Meta():
        model=Account
        fields = ['password']
