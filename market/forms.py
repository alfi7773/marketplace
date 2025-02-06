from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from market.models import *
from django.utils.translation import gettext_lazy as _

class ProfileChange(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email']

    widgets = {
                'username': forms.TextInput(attrs={'class': 'input-box', 'placeholder' : 'username'}),
                 'email': forms.EmailInput(attrs={'class': 'input-box', 'placeholder' : 'email'}),
                 'first_name' : forms.TextInput(attrs={'class': 'input-box', 'placeholder':'first_name'}),
                 'last_name' : forms.TextInput(attrs={'class': 'input-box', 'placeholder':'last_name'}),
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
        'class': 'width-form'
    }))


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    password1 = forms.CharField(label='Придумайте пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                validators=[validate_password])

    password2 = forms.CharField(label='Придумайте пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
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


#         def __init__(self, *args, **kwargs):
#                 super().__init__(*args, **kwargs)
#                 self.fields['first_name'].required = True
#                 self.fields['last_name'].required = True
#                 self.fields['email'].required = True

