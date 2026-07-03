from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdmin()]

    @extend_schema(
        request={"multipart/form-data": ProductImportSerializer},
        responses={202: None},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="import",
        permission_classes=[IsAdmin],
        parser_classes=[MultiPartParser, FormParser],
    )
    def import_products(self, request):
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