from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from billing.manager import PaymentTransactionManager
from billing.models import PaymentTransaction
from billing.serializers.transaction import TransactionSerializer


class BalanceAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user:
            return Response({
                'balance': request.user.get_balance()
            })

        return Response({'success': False}, status=401)


class RechargeAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user:
            try:
                PaymentTransactionManager.recharge(request.user, request.data['transaction_sum'])
                return Response({'success': True, 'balance': request.user.get_balance()}, status=200)
            except KeyError:
                Response({'success': False, 'message': 'Пропущено значение transaction_sum'}, status=400)

        return Response({'success': False}, status=401)


class TransactionsListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get(self, request):
        if request.user:
            transactions = PaymentTransaction.objects.filter(user=request.user)
            serializer = self.serializer_class(transactions, many=True)
            return Response(serializer.data, status=200)

        return Response({'success': False}, status=401)

    def post(self, request):
        if request.user:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                save_args = {'user': request.user}
                obj = serializer.save(**save_args)
                return Response(obj, 201)

        return Response({'success': False}, status=401)
