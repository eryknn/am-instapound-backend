from django.db import models

# Create your models here.
from model_utils.models import UUIDModel


class Picture(UUIDModel):
    uploaded_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='pictures',
        related_query_name='pictures'
    )
    picture = models.ImageField(upload_to='pictures')
    description = models.CharField(max_length=500, blank=True, default="")
    liked_by = models.ManyToManyField(
        'users.User',
        related_name='liked_pictures',
        related_query_name='liked_pictures'
    )


class PictureComment(UUIDModel):
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='picture_comments',
        related_query_name='picture_comments'
    )
    picture = models.ForeignKey(
        Picture,
        on_delete=models.CASCADE,
        related_name='picture_comments',
        related_query_name='picture_comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
