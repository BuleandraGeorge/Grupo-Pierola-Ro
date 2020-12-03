from allauth.account.forms import SignupForm
from .widgets import BootstrapDateTimePickerInput
from django import forms
from datetime import date

today = date.today()
c_year = today.year


class Age(forms.Form):
    date_of_birth = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=BootstrapDateTimePickerInput()
    )


class CustomForm(SignupForm, Age):
    date_of_birth = Age

    def signup(self, request, user):
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user

    field_order = ['date_of_birth', 'email', 'password1', 'password2']
