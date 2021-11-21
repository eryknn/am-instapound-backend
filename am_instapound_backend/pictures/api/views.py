from django.db.models import Count, Q
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from am_instapound_backend.pictures.api.permissions import IsPictureCommentCreatorOrReadOnly, IsPictureCreatorOrReadOnly
from am_instapound_backend.pictures.api.serializers import PictureListSerializer, PictureCreateSerializer, \
    PictureEditSerializer, PictureItemSerializer, PictureCommentCreateSerializer, PictureCommentEditSerializer
from am_instapound_backend.pictures.models import Picture, PictureComment


class PictureViewSet(ModelViewSet):
    model = Picture
    queryset = Picture.objects.all()
    serializer_class = PictureListSerializer
    permission_classes = [IsAuthenticated, IsPictureCreatorOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset().annotate(
            like_count=Count('liked_by'),
            is_liked=Count('liked_by', filter=Q(liked_by__id=self.request.user.id))
        )

        if self.action in ['retrieve', 'list']:
            qs.select_related('uploaded_by')

        if self.action == 'retrieve':
            qs.prefetch_related('picture_comments', 'picture_comments__created_by')

        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PictureItemSerializer
        if self.action == 'list':
            return PictureListSerializer
        if self.action == 'create':
            return PictureCreateSerializer
        if self.action in ['update', 'partial_update']:
            return PictureEditSerializer


class PictureCommentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    model = PictureComment
    serializer_class = PictureCommentCreateSerializer
    queryset = PictureComment.objects.all()
    permission_classes = [IsAuthenticated, IsPictureCommentCreatorOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return PictureCommentCreateSerializer
        if self.action in ['update', 'partial_update']:
            return PictureCommentEditSerializer
