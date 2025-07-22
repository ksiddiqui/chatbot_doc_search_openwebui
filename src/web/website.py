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
from fastapi.responses import HTMLResponse

from system.setup import get_config_logger


config, logger = get_config_logger()
router_prefix = config.get('web_prefix')
if router_prefix and len(router_prefix) > 0:
    router = APIRouter(prefix=router_prefix)
else:
    router = APIRouter()

@router.get("/")
async def serve_index():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        logger.error(f"Error in serve_index: {str(e)}")
        return HTMLResponse(content=f"<html><body><h1>Error loading index page</h1><p>{str(e)}</p></body></html>", status_code=500)
