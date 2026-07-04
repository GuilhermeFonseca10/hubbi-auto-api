from rest_framework import serializers


class ConsultantSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=True,
        max_length=1000,
    )