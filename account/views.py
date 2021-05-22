from django.contrib.auth import logout, login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User
from account.serializers.user import UserSerializer
from utils.utils import CsrfExemptSessionAuthentication


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                token, _ = user.generate_token()

                return JsonResponse({
                    'user': UserSerializer(instance=user).data,
                    'token': token.key
                }, status=200)

        except User.DoesNotExist:
            pass

        return JsonResponse({
            'non_field_error': 'Невозможно войти с предоставленными учетными данными',
            'errors': {
                'email': ['Поле заполнено неверно'],
                'password': ['Поле заполнено неверно']
            }
        }, status=400)


# class LogoutView(APIView):
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return JsonResponse({
#             'success': True
#         }, status=200)
#

@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data.get('password'))

        return JsonResponse({
            'user': UserSerializer(instance=user).data
        }, status=201)

# class RegistrationAPIView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = RegistrationSerializer
#     # renderer_classes = (UserJSONRenderer,)
#
#     def post(self, request):
#         user = request.data.get('user', {})
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=201)
#
#
# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     # renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         user = request.data.get('user', {})
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.data, status=200)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'message': 'e23'})