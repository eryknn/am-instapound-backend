import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from am_instapound_backend.users.managers import UserManager


class User(AbstractUser):
    objects = UserManager()  # we need custom UserManager because we do not have username field

    # we hold no personal info
    first_name = None
    last_name = None

    # we want primary key to be called id so need to ignore pylint
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # pylint: disable=invalid-name
    email = models.EmailField(_('Adres email'), blank=True, unique=True, null=True)  # type: ignore
    picture = models.ImageField(upload_to='profile-pic', null=True)

    class Meta(AbstractUser.Meta):
        abstract = False
        ordering = ('email', 'username')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
