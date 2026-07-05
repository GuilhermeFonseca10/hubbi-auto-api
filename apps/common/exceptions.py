from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    """Padroniza a resposta de exceção para a API.

    Args:
        exc: Exceção lançada pelo Django/DRF.
        context: Contexto da exceção.

    Returns:
        Response: Resposta DRF padronizada sem traceback.
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "detail": "Erro interno do servidor. Tente novamente mais tarde.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(exc, ValidationError):
        response.data = {
            "status_code": response.status_code,
            "detail": "Dados inválidos. Verifique os campos e tente novamente.",
            "errors": response.data,
        }
    else:
        detail = response.data.get("detail") if isinstance(response.data, dict) else None
        response.data = {
            "status_code": response.status_code,
            "detail": str(detail) if detail is not None else response.data,
        }

    return response
