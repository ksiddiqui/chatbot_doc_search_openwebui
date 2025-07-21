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

from system.setup import get_config_logger
from models.chat_completion import ChatRequest


class ChatCompletionService:
    def __init__(self):
        self.config, self.logger = get_config_logger()

    async def chat_completion_mock(self, req: ChatRequest):
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

    async def chat_completion(self, req: ChatRequest):
        try:
            last_msg = next(
                (m for m in reversed(req.messages) if m["role"] == "user"), None
            )
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

            print(json.dumps(req.model_dump()))
            query = last_msg["content"]

            # Extract conversation history for context
            conversation_history = get_last_n_pairs(req.messages, 3)
            model_id = req.model

            # Use default model if none provided or if invalid
            if not model_id:
                model_id = DEFAULT_MODEL_ID
                print(f"No model_id provided, using default: {model_id}")
            if not validate_model_id(model_id):
                print(f"Invalid model_id: {model_id}, using default: {DEFAULT_MODEL_ID}")
                model_id = DEFAULT_MODEL_ID
            try:
                inference_model = get_inference_model_from_id(model_id)
                print(
                    f"Using model_id: {model_id}, inference_model: {inference_model.value}"
                )
            except ValueError as ve:
                print(f"Model mapping error: {str(ve)}, using default: {DEFAULT_MODEL_ID}")
                model_id = DEFAULT_MODEL_ID
                inference_model = get_inference_model_from_id(model_id)

            rag = ContextualRAG(model_id=model_id)
            qa_agents = DocumentQAAgents(rag, model_id)

            result = await qa_agents.retrieve_answer_with_evaluation(
                query, conversation_history
            )
        except Exception as e:
            print("Exception: " + str(e))
            raise HTTPException(
                status_code=500, detail=f"Error during agentic query: {str(e)}"
            )
        
        return result