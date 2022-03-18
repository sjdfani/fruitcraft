from rest_framework import serializers
from .models import Account, Icons


class IconsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icons
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context['request']
        res = super().to_representation(instance)
        res['icon'] = IconsSerializer(
            instance.icon, context={'request': request}).data
        return res
