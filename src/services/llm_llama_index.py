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

from llama_index.llms.ollama import Ollama

from system.setup import get_config_logger

SUPPORTED_MODELS_TYPES = ['Ollama-Llama3']


class LLMManager:
    def __init__(self):
        self.config, self.logger = get_config_logger()
        self.llm = None
        self.llm_ollama_model = self.config['llm_ollama_model']
        self.llm_ollama_base_url = self.config['llm_ollama_base_url']

        self.is_llm_setup = False
        self.setup_llm()

    def setup_llm(self):
        if self.is_llm_setup:
            return self.llm

        self.llm = Ollama(
            model=self.llm_ollama_model,  # or specify a version, e.g., "llama2"
            base_url=self.llm_ollama_base_url,  # default Ollama endpoint
            temperature=0.3,
            request_timeout=60.0,
            # You can add additional parameters as needed
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
        response = self.llm.complete(prompt, **kwargs)
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