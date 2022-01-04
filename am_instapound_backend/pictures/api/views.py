from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from am_instapound_backend.pictures.api.permissions import IsPictureCommentCreatorOrReadOnly, IsPictureCreatorOrSafeOnly
from am_instapound_backend.pictures.api.serializers import PictureListSerializer, PictureCreateSerializer, \
    PictureEditSerializer, PictureItemSerializer, PictureCommentCreateSerializer, PictureCommentEditSerializer
from am_instapound_backend.pictures.models import Picture, PictureComment
from am_instapound_backend.utils.helpers import is_valid_uuid


class PictureViewSet(ModelViewSet):
    model = Picture
    queryset = Picture.objects.all()
    serializer_class = PictureListSerializer
    permission_classes = [IsAuthenticated, IsPictureCreatorOrSafeOnly]

    def get_queryset(self):
        qs = super().get_queryset().annotate(
            like_count=Count('liked_by', distinct=True),
            comment_count=Count('picture_comments', distinct=True),
            is_liked=Count('liked_by', filter=Q(liked_by__id=self.request.user.id))
        )

        if self.action in ['retrieve', 'list']:
            qs = qs.select_related('uploaded_by')

        if self.action == 'retrieve':
            qs = qs.prefetch_related('picture_comments', 'picture_comments__created_by')

        if (user_id := self.request.query_params.get('uploaded_by')) is not None and is_valid_uuid(user_id):
            qs = qs.filter(uploaded_by__id=user_id)

        return qs.order_by('-uploaded_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PictureItemSerializer
        if self.action == 'list':
            return PictureListSerializer
        if self.action == 'create':
            return PictureCreateSerializer
        if self.action in ['update', 'partial_update']:
            return PictureEditSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'uploaded_by', openapi.IN_QUERY, "Filter pictures by user", required=False, type=openapi.TYPE_STRING
        )
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request: Request, *args, **kwargs):
        picture: Picture = self.get_object()

        if self.request.method == 'POST':
            self.__like_picture(picture)
        else:
            self.__unlike_picture(picture)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def __like_picture(self, picture: Picture):
        if picture.liked_by.filter(pk=self.request.user.id).exists():
            raise ValidationError(detail=_('Picture is already liked.'))

        picture.liked_by.add(self.request.user)
        picture.save()

    def __unlike_picture(self, picture: Picture):
        if not picture.liked_by.filter(pk=self.request.user.id).exists():
            raise ValidationError(detail=_('Picture is not liked.'))

        picture.liked_by.remove(self.request.user)
        picture.save()


class PictureCommentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    model = PictureComment
    serializer_class = PictureCommentCreateSerializer
    queryset = PictureComment.objects.all().order_by('created_at')
    permission_classes = [IsAuthenticated, IsPictureCommentCreatorOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return PictureCommentCreateSerializer
        if self.action in ['update', 'partial_update']:
            return PictureCommentEditSerializer
