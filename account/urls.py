from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from account.views import LoginView, RegistrationView, HelloView

urlpatterns = [
    path('login/', csrf_exempt(LoginView.as_view()), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='logout'),
    path('hello/', HelloView.as_view(), name='logout'),
]
