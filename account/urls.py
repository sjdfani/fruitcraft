from django.urls import path
from .views import Accounts

app_name = 'account'

urlpatterns = [
    path('accounts/', Accounts.as_view()),
]
