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

from langchain_openai import ChatOpenAI

from system.setup import get_config_logger


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

        self.llm = ChatOpenAI(
            api_key=self.config['llm_openai_api_key'],
            model=self.config['llm_openai_model'],
            temperature=self.config['llm_openai_temperature'],
            max_tokens=self.config['llm_openai_max_tokens'],
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
        response = self.llm.invoke(prompt, **kwargs)
        response_content = response.content
        response_metadata = response.response_metadata
        
        return response_content

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

