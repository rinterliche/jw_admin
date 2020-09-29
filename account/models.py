from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class JWAdminCongregation(models.Model):
    """
    Structure for congregation model
    """
    class Meta:
        verbose_name = "Congregação"
        verbose_name_plural = "Congregações"

    name = models.CharField(max_length=50)

    def __str__(self):
        return "JWAdmin congregation: {}".format(self.name)


class JWAdminUserManager(BaseUserManager):
    """
    Structure for user manager model
    """
    class Meta:
        verbose_name = "Super user"
        verbose_name_plural = "Super users"

    def create_user(self, email, first_name, last_name, congregation, password=None):
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
            congregation=congregation,
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
            congregation=JWAdminCongregation.objects.get(id=1),
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class JWAdminUser(AbstractBaseUser):
    """
    Structure for user model
    """
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
    congregation = models.ForeignKey(
        JWAdminCongregation,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    objects = JWAdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        return "User name: {} email: {}".format(self.first_name, self.email)

    @staticmethod
    def has_perm():
        "Does the user have a specific permission?"
        return True

    @staticmethod
    def has_module_perms():
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
