from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from market.models import *

class ProfileChange(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email']

    widgets = {
                'username': forms.TextInput(attrs={'class': 'input-box', 'placeholder' : 'username', 'label': 'username'}),
                 'first_name' : forms.TextInput(attrs={'class': 'input-box', 'placeholder':'first_name', 'label':'first_name'}),
                 'last_name' : forms.TextInput(attrs={'class': 'input-box', 'placeholder':'last_name', 'label':'last_name'}),
                 'email': forms.EmailInput(attrs={'class': 'input-box', 'placeholder' : 'email', 'label':'email'}),
            }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['email'].required = True


class LoginForm(forms.Form):
    username = forms.CharField(label='имя пользователя', widget=forms.TextInput(attrs={
        'class': 'width-form', 'placeholder': 'username'
    }))

    password = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={
        'class': 'width-form', 'placeholder': 'password'
    }))


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'width-form', 'placeholder' : 'username'}),
             'email': forms.EmailInput(attrs={'class': 'width-form', 'placeholder' : 'email'}),
             'first_name' : forms.TextInput(attrs={'class': 'width-form', 'placeholder':'first_name'}),
             'last_name' : forms.TextInput(attrs={'class': 'width-form', 'placeholder':'last_name'}),
             'password1' : forms.PasswordInput(attrs={'class': 'input-box', 'placeholder':'password1'}),
             'password2' : forms.PasswordInput(attrs={'class': 'input-box', 'placeholder':'password2'})
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'width-form', 'placeholder': 'password1'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'width-form', 'placeholder': 'password2'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(1, 6)]),
        }


class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user: User = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(
        label='Old password',
        widget=forms.PasswordInput(attrs={'class': 'footer-display-col', 'placeholder': 'Old password'})
    )
    new_password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'width-form', 'placeholder': 'New Password'}),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'width-form', 'placeholder': 'Confirm password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        errors = {}

        if not self.user.check_password(old_password):
            errors['old_password'] = ['Old password is incorrect.']

        if new_password != confirm_password:
            errors['confirm_password'] = ['Passwords do not match.']

        if old_password == new_password:
            errors['new_password'] = ['New password must not be the same as the old password.']

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

