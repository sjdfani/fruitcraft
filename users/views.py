from users.models import CustomUser
from rest_framework.views import APIView
from .serializer import RegisterSerialzer, VerifyRegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import get_tokens_for_user


class Register(APIView):
    def post(self, request):
        serializer = RegisterSerialzer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)


class VerifyRegister(APIView):
    def post(self, request):
        serializer = VerifyRegisterSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                tokens = get_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                message = {'password': 'password is invalide.'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
