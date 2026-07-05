from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializador para o modelo de produto."""

    class Meta:
        model = Product
        fields = "__all__"


class ProductImportSerializer(serializers.Serializer):
    """Serializador para upload de arquivo CSV de importação."""

    file = serializers.FileField(
        help_text="Arquivo CSV contendo os campos nome, descricao, preco e quantidade_inicial.",
    )

    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError(
                "O arquivo deve estar no formato CSV."
            )

        return value