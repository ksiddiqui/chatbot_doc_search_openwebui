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

from fastapi import APIRouter
from typing import Any, Dict

from system.setup import get_config_logger
from services.chat_completion import ChatCompletionService
from models.chat_completion import ChatRequest, ChatCompletionResponse

config, logger = get_config_logger()
router_prefix = config.get('restapi_prefix')
if router_prefix and len(router_prefix) > 0:
    router = APIRouter(prefix=router_prefix)
else:
    router = APIRouter()

chat_completion_service = ChatCompletionService()


# Define available models
MODELS = [
    {"id": "Pak AI", "model": "pakai-2.1", "object": "model", "owned_by": "NorthBaySolutions"},
    # {"id": "AWS Bedrock", "model": "claude-3.5-sonnet", "object": "model", "owned_by": "anthropic"},
    # {"id": "OpenAI GPT", "model": "gpt-4", "object": "model", "owned_by": "openai"},
]

@router.get("/")
async def health() -> Dict[str, Any]:
    return {"status": True}
    
@router.get("/models")
async def models() -> Dict[str, Any]:
    return {"object": "list", "data": MODELS}

@router.get("/config")
async def get_config() -> Dict[str, Any]:
    return {"object": "config", "data": config}

@router.post("/chat/completions")
async def chat_completion(req: ChatRequest) -> Dict[str, Any]:
    result = chat_completion_service.chat_completion(req)
    return result
