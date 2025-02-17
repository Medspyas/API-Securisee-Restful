from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'age', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {
            'password': {'write_only': True},
            'id' : {'read_only': True},
            'email' : {'read_only': True}
        }

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError('Vous devez avoir au moins 15 ans pour vous inscrire.')
        return value
    
    def validate(self, data):
        if not data.get("can_be_contacted") and not data.get("can_data_be_shared"):
            raise serializers.ValidationError("Veuillez preciser une préférences de consentement")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        return super().update(instance, validated_data)
    
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get('request')
        if instance.can_data_be_shared is False:
            if request and request.user != instance and not request.user.is_superuser:

                data.pop('email', None)
                data.pop('age', None)
                data.pop('can_be_contacted', None)
                data.pop('can_data_be_shared', None)

        return data