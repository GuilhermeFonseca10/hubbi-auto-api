from apps.consultant.clients import GeminiClient
from apps.consultant.prompts import SYSTEM_PROMPT


class ConsultantService:

    def __init__(self):
        self.client = GeminiClient()

    def execute(self, message: str):

        prompt = f"""
            {SYSTEM_PROMPT}

            Pergunta:

            {message}
            """

        answer = self.client.generate(prompt)

        return {
            "answer": answer
        }