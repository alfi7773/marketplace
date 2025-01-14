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
                'username': forms.TextInput(attrs={'class': 'input-box', 'placeholder' : 'username'}),
                 'email': forms.EmailInput(attrs={'class': 'input-box', 'placeholder' : 'email'}),
                 'first_name' : forms.TextInput(attrs={'class': 'input-box', 'placeholder':'first_name'}),
                 'last_name' : forms.TextInput(attrs={'class': 'input-box', 'placeholder':'last_name'}),
            }



class LoginForm(forms.Form):
    username = forms.CharField(label='имя пользователя', widget=forms.TextInput(attrs={
        'class': 'width-form', 'placeholder': 'username'
    }))

    password = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={
        'class': 'width-form', 'placeholder': 'password'
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
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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

    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'width-form', 'placeholder': 'Старый пароль'}))
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'width-form', 'placeholder': 'Новый пароль'}),
                                                                                            validators=[validate_password])
    confirm_password = forms.CharField(label='Подтвердите пароль',
                                       widget=forms.PasswordInput(attrs={'class': 'width-form', 'placeholder': 'Подтвердите пароль'}))

    def clean(self):
        if self.is_valid():
            old_password, new_password, confirm_password = self.cleaned_data.values()

            errors = {}

            if not self.user.check_password(old_password):
                errors['old_password'] = ['Старый пароль неправильный.']


            if new_password != confirm_password:
                errors['confirm_password'] = ['Новые пароли не совпадают.']

            if old_password == new_password:
                errors['new_password'] = ['Новый пароль не может быть похож на первый.']

            if len(errors) > 0:
                raise forms.ValidationError(errors)

        return self.cleaned_data