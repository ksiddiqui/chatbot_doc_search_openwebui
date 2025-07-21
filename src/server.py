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

import sys
import os

# Add current directory to sys.path
sys.path.append(os.path.dirname(__file__))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from system.setup import do_setup
config, logger = do_setup()

from web.website import router as website_router
from web.chatbot_application import router as chat_app_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Serve static files - changed html=False to ensure the root handler is called
app.mount("/static", StaticFiles(directory="static", html=False), name="static")
# Mount the chat router
app.include_router(chat_app_router)
app.include_router(website_router)

logger.debug('FastAPI server is initialized and ready.')



if __name__ == "__main__":
    uvicorn.run(
        app=f"{__name__}:app", 
        host=config['fastapi_host'], 
        port=int(config['fastapi_port']), 
        reload=bool(config['fastapi_reload']), 
        use_colors=True,
    )
