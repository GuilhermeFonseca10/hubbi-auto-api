from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_spectacular.utils import extend_schema

from apps.integrations.permissions import HasApiKey
from apps.integrations.serializers import StockUpdateSerializer
from apps.integrations.services import StockIntegrationService


class IntegrationViewSet(ViewSet):

    permission_classes = [HasApiKey]

    @extend_schema(
        summary="Atualizar estoque via integração externa",
        description="Recebe uma lista de produtos com quantidades e atualiza o estoque no sistema.",
        request=StockUpdateSerializer,
        responses={
            200: {
                "description": "Estoque atualizado com sucesso.",
                "content": {
                    "application/json": {
                        "example": {"message": "Estoque atualizado com sucesso."}
                    }
                },
            }
        },
        tags=["Integrações"],
    )
    def create(self, request):

        serializer = StockUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        StockIntegrationService.execute(
            serializer.validated_data["products"]
        )

        return Response(
            {
                "message": "Estoque atualizado com sucesso."
            },
            status=status.HTTP_200_OK,
        )