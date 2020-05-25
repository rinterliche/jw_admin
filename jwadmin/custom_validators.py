import re
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    UserAttributeSimilarityValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext
from django.utils.translation import gettext as _, ngettext

from difflib import SequenceMatcher


class MinimumLengthValidator(MinimumLengthValidator):
    """
    Validate whether the password is of a minimum length.
    """

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Senha muito curta. A senha precisa ter no mínimo %(min_length)d caracter.",
                    "Senha muito curta. A senha precisa ter no mínimo  %(min_length)d caracteres.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Sua senha deve conter no mínimo %(min_length)d cararter.",
            "Sua senha deve conter no mínimo %(min_length)d caracteres.",
            self.min_length
        ) % {'min_length': self.min_length}


class UserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    """
    Validate whether the password is sufficiently different from the user's
    attributes.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("Senha é muito similar ao primeiro nome, último nome ou e-mail"),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _("Sua senha não pode ser muito similar a outros atributos.")


class CommonPasswordValidator(CommonPasswordValidator):
    """
    Validate whether the password is a common password.

    The password is rejected if it occurs in a provided list, which may be gzipped.
    The list Django ships with contains 1000 common passwords, created by Mark Burnett:
    https://xato.net/passwords/more-top-worst-passwords/
    """

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("Senha é muito comum."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Sua senha não pode ser muito comum.")


class NumericPasswordValidator(NumericPasswordValidator):
    """
    Validate whether the password is alphanumeric.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Senha não pode conter apenas números."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Senha não pode conter apenas números.")