from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20, label="Nazwa użytkownika",
                               widget=forms.TextInput(attrs={"class": "username"}))
    password1 = forms.CharField(label=("Hasło"), strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Potwierdź hasło"), widget=forms.PasswordInput, strip=False, help_text=(""))
    email = forms.EmailField(label='Adres e-mail')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
