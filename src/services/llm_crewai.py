# =============================================================================
# © 2025 Kashif Ali Siddiqui, Pakistan
# Developed by: Kashif Ali Siddiqui 
# Github: https://github.com/ksiddiqui
# LinkedIn: https://www.linkedin.com/in/ksiddiqui
# Email: kashif.ali.siddiqui@gmail.com
# Dated: July, 2025 
# -----------------------------------------------------------------------------
# This source code is the property of Kashif Ali Siddiqui and is confidential.
# Unauthorized copying or distribution of this file, via any medium, is strictly prohibited.
# =============================================================================

import requests
from crewai.llm import BaseLLM

from system.setup import get_config_logger


class OllamaLLM(BaseLLM):
    def __init__(self, model, base_url, temperature):
        self.model = model
        self.endpoint_chat = base_url + '/api/chat'
        self.endpoint_generate = base_url + '/api/generate'
        self.temperature = temperature

    def chat(self, messages, format=None, **kwargs):
        request_body = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": messages
                }
            ],
            "stream": False,
            "temperature": self.temperature
        }
        if format:
            request_body["format"] = format

        response = requests.post(self.endpoint_chat, json=request_body)
        response.raise_for_status()
        return response.json()["message"]["content"]

    def generate(self, messages, format=None, **kwargs):
        request_body = {
            "model": self.model,
            "prompt": messages,
            "stream": False,
            "temperature": self.temperature
        }
        if format:
            request_body["format"] = format
        response = requests.post(self.endpoint_generate, json=request_body)
        response.raise_for_status()
        return response.json()["message"]["response"]

    def call(self, messages, **kwargs):
        return self.chat(messages, **kwargs)


SUPPORTED_MODELS_TYPES = ['Ollama-Llama3']

class LLMManager:
    def __init__(self):
        self.config, self.logger = get_config_logger()
        self.llm = None
        self.llm_ollama_model = self.config['llm_ollama_model']
        self.llm_ollama_base_url = self.config['llm_ollama_base_url']
        self.llm_ollama_temperature = self.config['llm_ollama_temperature']
        self.llm_ollama_request_timeout = self.config['llm_ollama_request_timeout']

        self.is_llm_setup = False
        self.setup_llm()

    def setup_llm(self):
        if self.is_llm_setup:
            return self.llm

        self.llm = OllamaLLM(
            model=self.llm_ollama_model,
            base_url=self.llm_ollama_base_url,
            temperature=self.llm_ollama_temperature,
        )
        self.is_llm_setup = True
        return self.llm

    def get_models(self):
        return {"object": "list", "data": SUPPORTED_MODELS_TYPES}

    def predict(self, prompt: str, **kwargs):
        """
        CrewAI/LangChain compatible: Generate a response from the LLM given a prompt.
        """
        if not self.is_llm_setup:
            self.setup_llm()
        response = self.llm.chat(prompt, **kwargs)
        # If response is an object with .text, return that; otherwise, return as string
        return getattr(response, 'text', str(response))

    def __call__(self, prompt: str, **kwargs):
        """
        Alias for predict to maximize compatibility.
        """
        return self.predict(prompt, **kwargs)

    def invoke(self, prompt: str, **kwargs):
        """
        Optional: Some frameworks use invoke instead of predict/call.
        """
        return self.predict(prompt, **kwargs)

    def get_llm(self):
        return self.llm

