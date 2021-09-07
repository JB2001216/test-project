from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    USERNAME_FIELD: str = "email"
    email = models.EmailField("email address", unique=True)
    REQUIRED_FIELDS: List[str] = []
