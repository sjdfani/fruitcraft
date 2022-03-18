from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.core.mail import send_mail
from .models import CustomUser
from .utils import str_generator
from config.settings import Redis_object
from account.models import Account, AccountLevel, AccountInfo, AccountCards, Icons, Cards, StateAccountCards
from account.utils import create_default_cards


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

    def build_objects(self, email, password):
        user = CustomUser.objects.create(email=email, password=password)
        icon = Icons.objects.filter(name='orange').first()
        invite_code = str_generator(8)
        account = Account.objects.create(
            user=user, icon=icon, invite_code=invite_code)
        AccountLevel.objects.create(account=account)
        AccountInfo.objects.create(account=account)
        create_default_cards()
        card_1 = Cards.objects.filter(id=1).first()
        AccountCards.objects.create(
            account=account, card=card_1, power=200, price=200*6, state=StateAccountCards.BASKET
        )
        card_2 = Cards.objects.filter(id=2).first()
        AccountCards.objects.create(
            account=account, card=card_2, power=250, price=250*6, state=StateAccountCards.BASKET
        )
        card_3 = Cards.objects.filter(id=3).first()
        AccountCards.objects.create(
            account=account, card=card_3, power=180, price=180*6, state=StateAccountCards.BASKET
        )
        card_4 = Cards.objects.filter(id=4).first()
        AccountCards.objects.create(
            account=account, card=card_4, power=230, price=230*6, state=StateAccountCards.BASKET
        )

    def save(self, **kwargs):
        email = self.validated_data['email']
        redis_data_list = Redis_object.get(email).split('/')
        password = redis_data_list[1]
        self.build_objects(email, password)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise ValidationError('email is not exists.')
        return value
