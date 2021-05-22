from django.urls import path
from billing.views import TransactionsListView, BalanceAPIView, RechargeAPIView

urlpatterns = [
    path('transactions/', TransactionsListView.as_view(), name='transactions'),
    path('balance/', BalanceAPIView.as_view(), name='balance'),
    path('recharge/', RechargeAPIView.as_view(), name='recharge'),
]
