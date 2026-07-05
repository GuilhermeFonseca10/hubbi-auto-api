from rest_framework import serializers


class ConsultantSerializer(serializers.Serializer):
    """Serializador para a consulta ao consultor de IA."""

    message = serializers.CharField(
        required=True,
        max_length=1000,
        help_text="Mensagem do usuário para o consultor de IA.",
    )