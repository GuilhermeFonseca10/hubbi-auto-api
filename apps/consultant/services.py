from apps.products.models import Product
from apps.consultant.clients import GeminiClient
from apps.consultant.prompts import SYSTEM_PROMPT


class ConsultantService:

    def __init__(self):
        self.client = GeminiClient()

    def execute(self, message: str):

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

    def _get_products(self):
        return Product.objects.all()

    def _build_context(self, products):

        context = []

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
    ):

        return f"""
{SYSTEM_PROMPT}

Produtos disponíveis:

{context}

Pergunta do usuário:

{message}
"""