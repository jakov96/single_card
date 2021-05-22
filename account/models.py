from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token
from billing.manager import PaymentTransactionManager


class UserType:
    guest = 'guest'
    citizen = 'citizen'

    names = {
        guest: 'Гость',
        citizen: 'Житель'
    }
    choices = (
        (guest, names[guest]),
        (citizen, names[citizen]),
    )


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwars):
        if not email:
            raise ValueError('Необходимо указать Email')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email, password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта', blank=False, unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    user_type = models.CharField(verbose_name='Тип пользоватля', max_length=120, choices=UserType.choices,
                                 default=UserType.citizen)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        return self.email

    def generate_token(self):
        return Token.objects.get_or_create(user=self)

    class Meta:
        verbose_name_plural = 'Аккаунты'
        verbose_name = 'Аккаунт'

    def get_balance(self):
        return PaymentTransactionManager.get_balance(self)


User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False
User._meta.get_field('username')._unique = False
