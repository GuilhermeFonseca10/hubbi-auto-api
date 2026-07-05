from django.db import models


class Product(models.Model):
    """Representa um produto disponível na plataforma."""

    name = models.CharField(
        "Nome",
        max_length=255,
    )
    description = models.TextField(
        "Descrição",
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        "Preço",
        max_digits=10,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField(
        "Quantidade",
        default=0,
    )

    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
    )

    class Meta:
        app_label = "products"
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["name"]

    def __str__(self):
        return self.name

