from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.managers import UserManager
from core.models import TimeStampedModel
from core.utils import (
    validate_image_extension,
    validate_image_size
)

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(
        upload_to = 'avatar/',
        null=True, blank=True,
        validators=[validate_image_size, validate_image_extension]
    )

    is_staff = models.BooleanField(
        'Staff',
        default=False
    )
    is_active = models.BooleanField(
        'Active',
        default=True
    )
    is_superuser = models.BooleanField(
        'Superuser',
        default=False
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ('-created_at',)

    def has_perm(self, perm, obj = ...):
        return super().has_perm(perm, obj)
    
    def has_module_perms(self, app_label):
        return super().has_module_perms(app_label)