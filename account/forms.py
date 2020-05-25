from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _

from account.models import JWAdminUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, label="Email")
    email.widget.attrs.update(
        {"class": "form-control", "placeholder": "Digite seu email"})

    first_name = forms.CharField(max_length=50, label="Primeiro nome")
    first_name.widget.attrs.update(
        {"class": "form-control", "placeholder": "Digite seu primeiro nome"})

    last_name = forms.CharField(max_length=50, label="Último nome")
    last_name.widget.attrs.update(
        {"class": "form-control", "placeholder": "Digite seu último nome"})

    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password1.widget.attrs.update(
        {"class": "form-control", "placeholder": "Digite sua senha"})

    password2 = forms.CharField(label="Digite novamente sua senha", widget=forms.PasswordInput)
    password2.widget.attrs.update(
        {"class": "form-control", "placeholder": "Confirme sua senha"})

    class Meta:
        model = JWAdminUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",)


class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password.widget.attrs.update(
        {"class": "form-control", "required": True, "placeholder": "Digite sua senha"})

    email = forms.EmailField(label="Email")
    email.widget.attrs.update(
        {'class': 'form-control', 'required': True, "placeholder": "Digite seu email"})

    class Meta:
        model = JWAdminUser
        fields = (
            "email",
            "password")

    def clean(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Login inválido, confira o email ou o password.")
