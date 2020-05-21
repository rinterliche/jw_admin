from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext as _


class JWAdminUserManager(BaseUserManager):
    class Meta:
        verbose_name = "Suer user"
        verbose_name_plural = "Super users"

    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have an first name')
        if not last_name:
            raise ValueError('Users must have an last name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class JWAdminUser(AbstractBaseUser):
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    objects = JWAdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        return "JWAdmin user name: {} email: {}".format(self.first_name, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
