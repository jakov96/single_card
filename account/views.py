from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User, UserRegistrationConfirm, UserType
from account.serializers.user import UserSerializer, RegistrationUserSerializer, UserPasswordChangeSerializer
from utils.utils import CsrfExemptSessionAuthentication


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    Авторизация
    """
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(email=email, is_confirm=True)
            if user.check_password(password):
                token, _ = user.get_or_generate_token()

                return Response({
                    'user': UserSerializer(instance=user).data,
                    'token': token.key
                }, status=200)

        except User.DoesNotExist:
            pass

        return Response({
            'non_field_error': 'Невозможно войти с предоставленными учетными данными',
            'errors': {
                'email': ['Поле заполнено неверно'],
                'password': ['Поле заполнено неверно']
            }
        }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(APIView):
    """
    Регистрация
    """

    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    serializer_class = RegistrationUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data.get('password'))

        return Response({
            'user': UserSerializer(instance=user).data
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class ChangeUserPasswordView(APIView):
    """
    Изменение пароля
    """

    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    serializer_class = UserPasswordChangeSerializer

    def post(self, request):
        if request.user.is_authenticated:
            serializer = self.serializer_class(context={'request': request}, instance=self.request.user,
                                               data=request.data)

            if serializer.is_valid():
                user = self.request.user
                serializer.save()

                token, _ = user.get_or_generate_token()

                return Response({
                    'user': UserSerializer(instance=user).data,
                    'token': token.key
                }, status=200)

            return Response(serializer.errors, status=400)

        return Response({'success': False}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterConfirmView(APIView):
    """Подтверждение регистрации"""

    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)

    def post(self, request):
        email = request.data.get('email', '')
        code = int(request.data.get('code', 0))

        try:
            user = User.objects.get(email=email, is_confirm=False)
            user_registration_confirm = UserRegistrationConfirm.objects.filter(user=user, code=code,
                                                                               is_used=False).first()
            if user_registration_confirm:
                user.is_confirm = True
                user.save()

                user_registration_confirm.is_user = True
                user_registration_confirm.save()

                return Response({
                    'user': UserSerializer(instance=user).data
                }, status=201)

            return Response({
                'non_field_error': 'Не удалось подтвердить регистрацию',
                'errors': {
                    'email': ['Поле заполнено неверно'],
                    'code': ['Поле заполнено неверно']
                }
            }, status=400)

        except User.DoesNotExist:
            return Response({
                'non_field_error': 'Невозможно войти с предоставленными учетными данными',
                'errors': {
                    'email': ['Поле заполнено неверно'],
                    'password': ['Поле заполнено неверно']
                }
            }, status=400)


# TODO необходимо API Госуслуг
@method_decorator(csrf_exempt, name='dispatch')
class ESIAUserConfirmView(APIView):
    """Подтверждение пользователя с использованием ЕСИА"""

    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    serializer_class = UserSerializer

    def post(self, request):
        if self.request.user.is_authenticated:
            email = request.data.get('email', '')
            user_type = request.data.get('user_type', '')

            if user_type == UserType.citizen:
                try:
                    user = User.objects.get(email=email, is_confirm=True, is_esia_confirm=False, user_type=user_type)
                    user.is_esia_confirm = True
                    user.save()
                    serializer = self.serializer_class(user)

                    return Response(serializer.data, status=200)
                except User.DoesNotExist:
                    return Response({'success': False, 'message': 'Пользователь уже подтвержден'}, status=400)

            return Response({'success': False, 'message': 'Недопустимый тип пользователя'}, status=400)

        return Response({'success': False}, status=401)
