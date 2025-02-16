from openai import AzureOpenAI, OpenAI
import logging
import os

logger = logging.getLogger("mpf-utils.ai")

class OpenAIClient:
    def __init__(self, azure: bool = True, api_key: str = None, azure_endpoint: str = None, model:str = None, azure_openai_api_version: str = "2024-10-21"):
        self.azure = azure

        if self.azure:
            if not azure_endpoint:
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

            if not api_key:
                api_key = os.getenv("AZURE_OPENAI_API_KEY")

            self.deployment = azure_endpoint.split("/")[-3]
            self.model = self.deployment

            # cut the api version from the endpoint string
            self.api_version = azure_endpoint.split("=")[-1]


            self.client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=api_key,
                api_version=self.api_version,
            )

            logger.info(f"Using Azure OpenAI with:\nendpoint {azure_endpoint}\nendpoint model {self.model}\nendpoint api version {self.api_version}")

        else:
            if not api_key:
                api_key = os.getenv("OPENAI_API_KEY")

            self.model = model
            self.client = OpenAI(api_key=api_key)
            logger.info(f"Using OpenAI")

    def run_prompt(self, prompt: str, model: str = None) -> str:
        model = model or self.model
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error in AI client: {e}")
            return None
