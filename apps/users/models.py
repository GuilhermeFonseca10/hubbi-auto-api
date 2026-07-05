from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Modelo de usuário customizado com indicador administrativo."""

    is_admin = models.BooleanField(
        "É admin",
        default=False,
    )

    class Meta:
        app_label = "users"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["username"]
