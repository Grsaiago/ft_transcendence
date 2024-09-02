from django.db import models
from django.contrib.auth.models import AbstractUser


class TrUser(AbstractUser):
    # todos os campos de AbstractBaseUser
    profile_picture = models.TextField(
        verbose_name="base64 encoding of the user's pfp",
        null=True,
        blank=True,
        unique=False,
        default=None,
    )

# Create your models here.
