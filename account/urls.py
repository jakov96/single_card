from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from account.views import LoginView, RegistrationView, ChangeUserPasswordView, UserRegisterConfirmView

urlpatterns = [
    path('login/', csrf_exempt(LoginView.as_view()), name='login'),
    path('registration/', RegistrationView.as_view(), name='logout'),
    path('change_password/', ChangeUserPasswordView.as_view(), name='change_password'),
    path('confirm/', UserRegisterConfirmView.as_view(), name='change_password'),
]
