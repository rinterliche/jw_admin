from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db.utils import OperationalError

from account.models import JWAdminUser, JWAdminCongregation


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, label="Email")
    email.widget.attrs.update(
        {"class": "form-control", "placeholder": "Digite seu email", "autocomplete": "off"})

    first_name = forms.CharField(max_length=50, label="Primeiro nome")
    first_name.widget.attrs.update(
        {"class": "form-control", "placeholder": "Digite seu primeiro nome", "autocomplete": "off"})

    last_name = forms.CharField(max_length=50, label="Último nome")
    last_name.widget.attrs.update(
        {"class": "form-control", "placeholder": "Digite seu último nome", "autocomplete": "off"})

    try:
        congregation_choises = [(congregation.id, congregation.name)
                                for congregation in JWAdminCongregation.objects.all()]
    except OperationalError:
        congregation_choises = []

    congregation = forms.ChoiceField(
        label="Congregação", choices=[(0, 'Selecione sua congregação')] +
        congregation_choises
    )
    congregation.widget.attrs.update(
        {"class": "form-control"})

    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password1.widget.attrs.update(
        {"class": "form-control", "placeholder": "Digite sua senha", "autocomplete": "off"})

    password2 = forms.CharField(label="Digite novamente sua senha", widget=forms.PasswordInput)
    password2.widget.attrs.update(
        {"class": "form-control", "placeholder": "Confirme sua senha", "autocomplete": "off"})

    class Meta:
        model = JWAdminUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "congregation",
            "password1",
            "password2",)

    def clean_congregation(self):
        congregation_id = self.cleaned_data['congregation']
        congregation = JWAdminCongregation.objects.get(id=congregation_id)
        return congregation


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
