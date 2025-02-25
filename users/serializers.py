from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # Représente l'objet utilisateur qui sera converti en format json,,
    # pour être envoyé à la base de données.
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "email": {"read_only": True},
        }

    def validate_age(self, value):
        # Vérification de l'âge de l'utilisateur avant son inscription.
        if value < 15:
            raise serializers.ValidationError(
                "Vous devez avoir au moins 15 ans pour vous inscrire."
            )
        return value

    def validate(self, data):
        # Vérification des champs contact et partage de données, qu'ils ai obligatoirement une valeur.
        if not data.get("can_be_contacted") and not data.get("can_data_be_shared"):
            raise serializers.ValidationError(
                "Veuillez preciser une préférences de consentement"
            )
        return data

    def create(self, validated_data):
        # Création de l'utilisateur avec un mot de passe haché.
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        # Permet de modifier les infos de l'utilisateur.
        validated_data.pop("password", None)
        return super().update(instance, validated_data)
