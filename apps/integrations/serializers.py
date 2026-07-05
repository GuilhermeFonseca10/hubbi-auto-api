from rest_framework import serializers


class StockItemSerializer(serializers.Serializer):
    """Serializador para cada item de estoque enviado pela integração."""

    id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=0)


class StockUpdateSerializer(serializers.Serializer):
    """Serializador para o payload de atualização de estoque."""

    products = StockItemSerializer(many=True)