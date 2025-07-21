# =============================================================================
# © 2025 Kashif Ali Siddiqui, Pakistan
# Developed by: Kashif Ali Siddiqui 
#
# Github: https://github.com/ksiddiqui
# LinkedIn: https://www.linkedin.com/in/ksiddiqui
# Email: kashif.ali.siddiqui@gmail.com
# Dated: July, 2025 
# -----------------------------------------------------------------------------
# This source code is the property of Kashif Ali Siddiqui and is confidential.
# Unauthorized copying or distribution of this file, via any medium, is strictly prohibited.
# =============================================================================

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    model: str
    messages: list


class RAGRequest(BaseModel):
    query: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class ChatUsage(BaseModel):
    metadata: Dict[str, Any] = {}
    sources: List[Any] = []


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    choices: List[ChatChoice]
    usage: ChatUsage
    
    @classmethod
    def create_response(cls, result: Dict[str, Any]) -> 'ChatCompletionResponse':
        message = ChatMessage(
            role="assistant",
            content=result.get("final_answer", "Unable to find the answer.")
        )
        
        choice = ChatChoice(
            index=0,
            message=message,
            finish_reason="stop"
        )
        
        usage = ChatUsage(
            metadata=result.get("metadata", {}),
            sources=result.get("sources", [])
        )
        
        return cls(
            id="chatcmpl-agentic",
            object="chat.completion",
            choices=[choice],
            usage=usage
        )