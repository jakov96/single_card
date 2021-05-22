from random import randint
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import get_template
from django.conf import settings
from rest_framework.authtoken.models import Token
from billing.manager import PaymentTransactionManager
from catalog.models import Achievement


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
    def create_user(self, email, name=None, user_type=None, password=None, **kwars):
        if not email:
            raise ValueError('Необходимо указать Email')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)

        user_registration_confirm = UserRegistrationConfirm.objects.create(
            user=user
        )
        user_registration_confirm.send_email()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    name = models.CharField(verbose_name='Имя', max_length=200, null=True, blank=True)
    email = models.EmailField(verbose_name='Электронная почта', blank=False, unique=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    user_type = models.CharField(verbose_name='Тип пользоватля', max_length=120, choices=UserType.choices,
                                 default=UserType.citizen, null=True, blank=True)
    is_confirm = models.BooleanField(verbose_name='Подтвержден?', default=False)
    achievements = models.ManyToManyField(Achievement, verbose_name='Достижения', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_or_generate_token(self):
        return Token.objects.get_or_create(user=self)

    def refresh_token(self):
        token = self.get_or_generate_token()
        token.delete()
        return self.get_or_generate_token()

    class Meta:
        verbose_name_plural = 'Аккаунты'
        verbose_name = 'Аккаунт'

    def get_balance(self):
        return PaymentTransactionManager.get_balance(self)


class UserRegistrationConfirm(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    code = models.IntegerField(verbose_name='Код')

    class Meta:
        verbose_name = 'Запрос на подтверждение регистрации'
        verbose_name_plural = 'Запросы на подтверждение регистрации'

    @classmethod
    def generate_code(cls):
        return randint(10000, 99999)

    @classmethod
    def generate_test_code(cls):
        return 77777

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_test_code()

        super().save(*args, **kwargs)

    def send_email(self):
        try:
            theme = "Подтверждение регистрации в системе 'Единая карта'"
            t = get_template('mail/user_registration_confirm.html')
            html_content = t.render({
                'site_domain': settings.DOMAIN_URL,
                'code': self.code,
            })
            msg = EmailMultiAlternatives(theme, html_content, settings.EMAIL_HOST, [self.user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        except Exception:
            pass


User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False
User._meta.get_field('username')._unique = False
