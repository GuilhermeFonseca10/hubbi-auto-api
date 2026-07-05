from typing import Iterable, List

from apps.products.models import Product
from apps.consultant.clients import GeminiClient
from apps.consultant.prompts import SYSTEM_PROMPT


class ConsultantService:
    """Service que monta contexto de produtos e consulta o modelo Gemini."""

    def __init__(self) -> None:
        self.client = GeminiClient()

    def execute(self, message: str) -> dict:
        """Executa a requisição ao consultor de IA.

        Args:
            message: Mensagem do usuário.

        Returns:
            dict: Resposta com o texto gerado pela IA.
        """

        products = self._get_products()
        context = self._build_context(products)

        prompt = self._build_prompt(
            context=context,
            message=message,
        )

        answer = self.client.generate(prompt)

        return {
            "answer": answer
        }

    def _get_products(self) -> Iterable[Product]:
        return Product.objects.all()

    def _build_context(self, products: Iterable[Product]) -> str:
        """Monta o contexto de produtos para enviar ao modelo de IA."""

        context: List[str] = []

        for product in products:
            context.append(
                f"""
Nome: {product.name}
Descrição: {product.description}
Preço: R$ {product.price}
Quantidade: {product.quantity}
                """.strip()
            )

        return "\n\n------------------------\n\n".join(context)

    def _build_prompt(
        self,
        context: str,
        message: str,
    ) -> str:
        """Constrói o prompt final a ser enviado para a Gemini."""

        return f"""
{SYSTEM_PROMPT}

Produtos disponíveis:

{context}

Pergunta do usuário:

{message}
"""