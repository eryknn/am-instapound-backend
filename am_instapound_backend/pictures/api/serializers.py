from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from am_instapound_backend.pictures.models import Picture, PictureComment
from am_instapound_backend.users.api.serializers import UserMinimalSerializer


class PictureCommentCreateSerializer(ModelSerializer):
    class Meta:
        model = PictureComment
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at', 'id']

    def save(self, **kwargs):
        return super().save(created_by=self.context['request'].user, **kwargs)


class PictureCommentEditSerializer(PictureCommentCreateSerializer):
    class Meta(PictureCommentCreateSerializer.Meta):
        read_only_fields = PictureCommentCreateSerializer.Meta.read_only_fields + ['picture']


class PictureCommentReadSerializer(ModelSerializer):
    created_by = UserMinimalSerializer(many=False, read_only=True)

    class Meta:
        model = PictureComment
        fields = ['id', 'created_by', 'updated_at', 'created_at', 'content']
        read_only_fields = fields


class PictureEditSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = ['description']


class PictureCreateSerializer(PictureEditSerializer):
    picture_message = _("Rozmiar zdjęcia nie powinien przekraczać 1Mb")

    class Meta(PictureEditSerializer.Meta):
        fields = PictureEditSerializer.Meta.fields + ['picture']

    def validate_picture(self, value):
        value: InMemoryUploadedFile
        if value.size > 1000000:  # 1mb, optymalizacja listy zdjęć
            raise ValidationError(self.picture_message, code='size_exceeded')
        return value

    def save(self, **kwargs):
        return super().save(uploaded_by=self.context['request'].user, **kwargs)


class PictureListSerializer(PictureCreateSerializer):
    like_count = SerializerMethodField()
    is_liked = SerializerMethodField()
    uploaded_by = UserMinimalSerializer(many=False, read_only=True)

    class Meta(PictureCreateSerializer.Meta):
        fields = PictureCreateSerializer.Meta.fields + ['id', 'like_count', 'is_liked', 'uploaded_by']
        read_only_fields = fields

    def get_is_liked(self, picture: Picture):
        return bool(picture.is_liked)

    def get_like_count(self, picture: Picture):
        return picture.like_count


class PictureItemSerializer(PictureListSerializer):
    picture_comments = PictureCommentReadSerializer(many=True, read_only=True)

    class Meta(PictureListSerializer.Meta):
        fields = PictureListSerializer.Meta.fields + ['picture_comments']
        read_only_fields = fields
