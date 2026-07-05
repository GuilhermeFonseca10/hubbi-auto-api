from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from apps.products.services import ProductImportService
from apps.products.tasks import import_products_task
from drf_spectacular.utils import extend_schema

from apps.products.models import Product
from apps.products.serializers import ProductSerializer, ProductImportSerializer
from apps.common.permissions import IsAdmin


class ProductViewSet(ModelViewSet):
    """ViewSet que expõe CRUD de produtos e upload de CSV."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        if self.action in ["create", "update", "partial_update", "destroy", "import_products"]:
            return [IsAdmin()]
        return super().get_permissions()

    @extend_schema(
        summary="Importar produtos via CSV",
        description="Recebe um arquivo CSV e inicia a importação assíncrona de produtos.",
        request={"multipart/form-data": ProductImportSerializer},
        responses={
            202: {
                "description": "Importação agendada com sucesso.",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Arquivo recebido. A importação foi iniciada."
                        }
                    }
                },
            }
        },
        tags=["Produtos"],
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="import",
        permission_classes=[IsAdmin],
        parser_classes=[MultiPartParser, FormParser],
    )
    def import_products(self, request):
        """Recebe o upload CSV e enfileira a task de importação."""
        serializer = ProductImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        file_path = ProductImportService.save_uploaded_file(file)

        import_products_task.delay(file_path)

        return Response(
            {
                "message": "Arquivo recebido. A importação foi iniciada."
            },
            status=status.HTTP_202_ACCEPTED,
        )