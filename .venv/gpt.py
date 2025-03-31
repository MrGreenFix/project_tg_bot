import openai
import httpx
import config
import os


openai_client = openai.AsyncOpenAI(api_key=config.TOKEN_OPENAI)
TOKEN_OPENAI = 'sk-proj-' + config.TOKEN_OPENAI[:3:-1] if config.TOKEN_OPENAI.startswith('gpt:') else config.TOKEN_OPENAI


class ChatGptService:
    def __init__(self, api_client):
        self.api_client = api_client

    async def send_message(self, prompt: str = "", user_message: str = "") -> str:
        messages = []
        if user_message:
            messages.append({"role": "user", "content": user_message})
        if prompt:
            messages.append({"role": "system", "content": prompt})

        response = await self.api_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )

        return response.choices[0].message.content


gpt_service = ChatGptService(openai_client)