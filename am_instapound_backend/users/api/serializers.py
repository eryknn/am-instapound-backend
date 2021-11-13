from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserProfileReadSerializer(serializers.ModelSerializer):
    picture_message = _("Rozmiar zdjęcia nie powinien przekraczać 1Mb")

    class Meta:
        model = User
        fields = ["id", "username", "picture"]

    def validate_picture(self, value):
        value: InMemoryUploadedFile
        if value.size > 1000000:  # 1mb - do zdjęcia profilowego, będzie ich dużo na liście komentarzy, nie chcemy mulić
            raise ValidationError(self.picture_message, code='size_exceeded')
        return value


class ProfilePictureUploadSerializer(serializers.ModelSerializer):
    picture_message = _("Rozmiar zdjęcia nie powinien przekraczać 1Mb")

    class Meta:
        model = User
        fields = ["picture"]

    def validate_picture(self, value):
        value: InMemoryUploadedFile
        if value.size > 1000000:  # 1mb - do zdjęcia profilowego, będzie ich dużo na liście komentarzy, nie chcemy mulić
            raise ValidationError(self.picture_message, code='size_exceeded')
        return value


class RegistrationSerializer(serializers.Serializer):
    email_message = _("Ten email jest już zajęty!")
    password_message = _("Hasło i potwierdź hasło musza byc identyczne.")

    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message=email_message)]
    )
    username = serializers.CharField(required=True, min_length=5, max_length=150)
    password = serializers.CharField(required=True, min_length=8, max_length=128, write_only=True)
    confirm_password = serializers.CharField(required=True, min_length=8, max_length=128, write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs.get('password') != attrs.pop('confirm_password'):
            raise ValidationError({
                'password': [self.password_message],
                'confirm_password': [self.password_message]
            }, code='not_identical')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password')
        )

    def update(self, instance, validated_data):
        raise NotImplementedError('Registration does not support updating')
