from rest_framework import serializers


class StockItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=0)


class StockUpdateSerializer(serializers.Serializer):
    products = StockItemSerializer(many=True)