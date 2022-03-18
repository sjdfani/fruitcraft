from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from account.models import Account
from .serializer import AccountSerializer


class Accounts(ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
