from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User
from account.serializers.user import UserSerializer, RegistrationUserSerializer, UserPasswordChangeSerializer
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
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
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
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    parser_classes = (JSONParser,)
    serializer_class = UserPasswordChangeSerializer

    def post(self, request):
        if request.user.is_authenticated:
            serializer = self.serializer_class(context={'request': request}, instance=self.request.user, data=request.data)
            if serializer.is_valid():
                user = self.request.user
                serializer.save()
                token, _ = user.get_or_generate_token()

                return Response({
                    'user': UserSerializer(instance=user).data,
                    'token': token.key
                }, status=200)

        return Response({'success': False}, status=401)