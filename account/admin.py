from django.contrib import admin
from account.models import User, UserRegistrationConfirm

admin.site.register(User)
admin.site.register(UserRegistrationConfirm)
