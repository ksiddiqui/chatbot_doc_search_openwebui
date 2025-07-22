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

from typing import List, Tuple, Dict, Any
import json

from fastapi import HTTPException

from services.observability import observability_reset
from system.setup import get_config_logger
from models.chat_completion import ChatRequest, ChatCompletionResponse
from services.llm_langchain import LLMManager
from services.rag import RAGManager
from services.multi_agents import MultiAgentsManager
from services.query_preprocessor import QueryPreprocessor

from services.observability import observability_reset, observability_set_question, observability_evaluate_now, observability_set_answer


class ChatCompletionService:
    def __init__(self):
        self.config, self.logger = get_config_logger()
        self.model_id = 'Ollama'
        self.inference_model = self.config["llm_ollama_model"]

        self.llm_manager = LLMManager()            
        self.rag_manager = RAGManager()
        self.multi_agent_system = MultiAgentsManager(self.rag_manager, self.llm_manager)
        self.query_preprocessor = QueryPreprocessor(self.llm_manager)

    def chat_models(self):
        return {"object": "list", "data": ['Ollama']}

    def chat_completion_mock(self, dialogue: ChatRequest):
        self.logger.info("Mocked chat completion")
        return {
            "id": "mocked",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Mocked response",
                    },
                    "finish_reason": "stop",
                }
            ],
        }

    def _process_query_when_inappropriate(self, evaluation_result):
        response = {
            "final_answer": evaluation_result.get("generated_query", "Your query is inappropriate. I can only help with questions related to the business domain."),
            "sources": "",
            "metadata": {
                "evaluation": evaluation_result,
                "flow_type": "inappropriate_question",
                "model_id": self.model_id,
                "inference_model": self.inference_model,
            },
        }
        if not response.get("final_answer") or len(response.get("final_answer").strip()) == 0:
            response["final_answer"] = "Your query is inappropriate. I can only help with questions related to the business domain."
        
        return response

    def _process_query_when_greeting(self, evaluation_result):
        response = {
            "final_answer": evaluation_result.get("generated_query", "Hello! I'm your AI Assistant, here to help."),
            "sources": "",
            "metadata": {
                "flow_type": "greeting",
                "model_id": self.model_id,
                "inference_model": self.inference_model,
            },
        }
        if not response.get("final_answer") or len(response.get("final_answer").strip()) == 0:
            response["final_answer"] = "Hello human! I'm your AI Assistant. How can I help you with your query?"
        
        return response

    def _process_query_when_other(self, evaluation_result):
        response = {
            "final_answer": evaluation_result.get("generated_query", "Unable to understand your query. I can only help with questions related to the business domain."),
            "sources": "",
            "metadata": {
                "flow_type": "other",
                "model_id": self.model_id,
                "inference_model": self.inference_model,
            },
        }
        if not response.get("final_answer") or len(response.get("final_answer").strip()) == 0:
            response["final_answer"] = "Unable to understand your query. I can only help with questions related to the business domain."
        
        return response
    
    def _process_query_normal(self, evaluation_result, question, multi_agent_system):
        optimized_query = evaluation_result.get("generated_query", question)

        self.logger.info(f"Original question: {question}")
        self.logger.info(f"Optimized query: {optimized_query}")

        if not optimized_query or len(optimized_query.strip()) == 0:
            optimized_query = question

        observability_reset()
        observability_set_question(optimized_query)

        result = self.multi_agent_system.answer_question(optimized_query)
        if not result:
            result = {
                "final_answer": "Unable to find the answer.",
                "sources": "",
                "metadata": {
                    "evaluation": evaluation_result,
                    "flow_type": "crew_agents",
                    "original_question": question,
                    "optimized_query": optimized_query,
                    "model_id": self.model_id,
                    "inference_model": self.inference_model,
                },
            }
        original_metadata = result.get("metadata", "") if result else {}

        observability_set_answer(result.get("final_answer", ""))
        observability_evaluate_now()

        # raise Exception("test")
        response = {
            "final_answer": result.get("final_answer", ""),
            "sources": result.get("sources", ""),
            "metadata": {
                "evaluation": evaluation_result,
                "flow_type": "crew_agents",
                "original_question": question,
                "optimized_query": optimized_query,
                "crew_validation": original_metadata,
                "model_id": self.model_id,
                "inference_model": self.inference_model,
            },
        }
        return response

    def chat_completion(self, dialogue: ChatRequest):
        result = None
        try:
            last_msg = next((m for m in reversed(dialogue.messages) if m["role"] == "user"), None)
            if not last_msg:
                raise HTTPException(status_code=400, detail="No user message provided.")

            # Skip internal follow-up / title / tag tasks
            if "### Task:" in last_msg["content"]:
                return {
                    "id": "skipped",
                    "object": "chat.completion",
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": "System task skipped by API",
                            },
                            "finish_reason": "stop",
                        }
                    ],
                }

            self.logger.info(f"Dialogue model request: {json.dumps(dialogue.model_dump())}")
            query = last_msg["content"]
            model_id = dialogue.model

            # Extract conversation history for context
            conversation_history = self._get_last_n_pairs(dialogue.messages, 3)
            if conversation_history is None:
                conversation_history = []            
            
            preprocessing_result = self.query_preprocessor.evaluate_question(query, conversation_history)
            if preprocessing_result["type"] == "inappropriate":
                response = self._process_query_when_inappropriate(preprocessing_result)
            elif preprocessing_result["type"] == "greeting":
                response = self._process_query_when_greeting(preprocessing_result)
            elif preprocessing_result["type"] == "other":
                response = self._process_query_when_other(preprocessing_result)
            else:
                response = self._process_query_normal(preprocessing_result, query, self.multi_agent_system)

            result = self._prepare_result(response)
            
        except Exception as e:
            self.logger.error("Exception: " + str(e))
            raise HTTPException(
                status_code=500, detail=f"Error during agentic query: {str(e)}"
            )
        
        return result

    def _prepare_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        response_dict = {
            "id": "chatcmpl-agentic",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": result.get(
                            "final_answer", "Unable to find the answer."
                        ),
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "metadata": result.get("metadata", {}),
                "sources": result.get("sources", []),
            },
        }

        return response_dict

    def _get_last_n_pairs(self, messages: list, n: int = 3) -> list:
        conversation_history = []
        for i in range(len(messages) - 2, 0, -1):
            if len(conversation_history) >= n:
                break
            if (i > 0 and messages[i]["role"] == "assistant" and messages[i-1]["role"] == "user"):
                conversation_history.append({
                    "question": messages[i-1]["content"], 
                    "answer": messages[i]["content"]
                })
        return list(reversed(conversation_history))