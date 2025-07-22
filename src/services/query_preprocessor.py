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

from typing import Optional, List, Dict, Any

from system.setup import get_config_logger
from services.llm_langchain import LLMManager
# from services.llm_llama_index import LLMManager
from system.data import convert_to_json

class QueryPreprocessor:
    def __init__(self, llm_manager: LLMManager):
        self.config, self.logger = get_config_logger()
        self.llm_manager = llm_manager
        self.llm = self.llm_manager # self.llm_manager.get_llm()
        self.model_id = 'Ollama'
        self.inference_model = self.config["llm_ollama_model"]
        self.business_domain = self.config["business_domain"]

    def evaluate_question(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        fallback_result = {
            "type": "question",
            "reason": "Evaluation failed.",
            "generated_query": query,
        }

        formatted_history = self._format_conversation_history(conversation_history)
        evaluation_prompt = self._get_evaluation_prompt(
                variables={
                    "business_domain": self.business_domain,
                    "history": formatted_history,
                    "question": query,
                }
            )
        
        eval_response = self.llm.predict(evaluation_prompt)
        eval_response_text = eval_response.content if hasattr(eval_response, "content") else str(eval_response)

        eval_response_json = convert_to_json(eval_response_text, force_find_json=True)
        if eval_response_json is None:
            fallback_result["reason"] = fallback_result["reason"] + f" Failed to convert response to JSON."
            return fallback_result

        required_fields = ["type", "reason"]
        for field in required_fields:
            if field not in eval_response_json:
                fallback_result["reason"] = fallback_result["reason"] + f" Missing required field: {field}"
                return fallback_result
        
        return eval_response_json


    def _format_conversation_history(self, conversation_history: List[Dict[str, str]]) -> str:
        formatted_history = []
        for conv in conversation_history:
            formatted_history.append(f"""<conversation>
<question>{conv["question"]}</question>
<answer>{conv["answer"]}</answer>
</conversation>""")

        return "\n".join(formatted_history)

    def _get_evaluation_prompt(self, variables: Dict[str, Any]) -> str:
        prompt = """
You are a highly intelligent assistant trained to evaluate user messages in a business context.  
You will be given:
1. A **user question**
2. **Conversation history** as context
3. A **business domain** in which the conversation takes place

Your task is to:

1. **Classify** the nature of the input — whether it's a:
   - "question" (e.g., a request for information or clarification),
   - "greeting" (e.g., "hello", "good morning"),
   - "inappropriate" (e.g., "I want to know your private information", "You are a bad person"),
   - "other" (anything that doesn't fit the above).
2. **Justify your decisions** for both appropriateness and classification.
3. Based on the classification, 
    - If it is a **question**, generate an **optimized version** of the query that incorporates the context from the conversation history for better clarity and relevance. 
    - Otherwise, give me an adequate responsee to the user. Also greet back if the user greets earlier.

---

**Input Format:**
Question:
{question}

Conversation History:
{history}

Business Domain:
{business_domain}

---

**Output Format (strict JSON):**
{{
  "type": "question",
  "reason": "The question builds upon the previous conversation about invoice generation and fits within the domain of enterprise finance tools.",
  "generated_query": "How can we automate invoice generation for recurring clients using our current enterprise finance tool?"
}}

---

Instructions:
- Be concise but precise in your classifications.
- Use the business domain and conversation history as critical context for evaluation.
- If no query optimization is needed, repeat the question in "generated_query".
- If input type is not "question", set "generated_query" to null.
"""
        filled_prompt = prompt.format(**variables)
        return filled_prompt
