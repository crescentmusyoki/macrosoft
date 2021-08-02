from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from calculator.models import Calculation


class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label='Password')

    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=55, required=True, label='First name')
    last_name = forms.CharField(max_length=55, required=True, label='Last name')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label='Password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password',)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=55, required=True, label='First name')
    last_name = forms.CharField(max_length=55, required=True, label='Last name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ('calculation_expression',)

    def __init__(self, *args, **kwargs):
        super(CalculationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
