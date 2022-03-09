from django.urls import path
from .views import Register, VerifyRegister, Login

app_name = 'users'

urlpatterns = [
    path('register/', Register.as_view()),
    path('register/verify/', VerifyRegister.as_view()),
    path('login/', Login.as_view()),
]
