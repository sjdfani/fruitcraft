from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.core.mail import send_mail
from .models import CustomUser
from .utils import str_generator
from config.settings import Redis_object
from account.models import Account, AccountLevel, AccountInfo,AccountCards


class RegisterSerialzer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('email is exists.')
        return value

    def save(self, **kwargs):
        email = self.validated_data['email']
        password = self.validated_data['password']
        rand_str = str_generator(6)
        Redis_object.set(email, f'{rand_str}/{password}', ex=3600)
        message = f"Your code : {rand_str}\nPlease set it in code lineEdit."
        send_mail('Verify', message, 'faniamtest@gmail.com', [email])


class VerifyRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('email is exists.')
        return value

    def validate(self, attrs):
        email = attrs['email']
        redis_data = Redis_object.get(email)
        if redis_data is not None:
            redis_data_list = redis_data.split('/')
            if redis_data_list[0] != attrs['code']:
                raise ValidationError('code is invalide.')
            return attrs
        else:
            raise ValidationError('code was expired.')

    def save(self, **kwargs):
        email = self.validated_data['email']
        redis_data_list = Redis_object.get(email).split('/')
        password = redis_data_list[1]
        user = CustomUser.objects.create(email=email, password=password)
        # create model for account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise ValidationError('email is not exists.')
        return value
