from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from apps.consultant.serializers import ConsultantSerializer
from apps.consultant.services import ConsultantService


class ConsultantViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Consulta de IA para recomendação de peças",
        description="Envia a mensagem do cliente ao consultor de IA e retorna uma resposta baseada no catálogo de produtos.",
        request=ConsultantSerializer,
        responses={
            200: {
                "description": "Resposta gerada pelo consultor de IA.",
                "content": {
                    "application/json": {
                        "example": {"answer": "Sugestão de peça para o cliente..."}
                    }
                },
            }
        },
        tags=["Consultor"],
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="",
    )
    def consult(self, request):
        serializer = ConsultantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ConsultantService()

        response = service.execute(
            serializer.validated_data["message"]
        )

        return Response(
            response,
            status=status.HTTP_200_OK,
        )