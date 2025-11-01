from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="Multi AI Agent LLMOPS API", version="1.0.0")

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool = False


@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    Endpoint to handle chat requests using multiple AI agents.
    """
    logger.info(f"Received chat request with model: {request.model_name}")
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning(f"Model {request.model_name} is invalid.")
        raise HTTPException(status_code=400, detail="Invalid model name provided.")
    try:
        
        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )
        logger.info(f"Successfully got  response from AI agents {request.model_name}")

        return {"response": response}
    except CustomException as ce:
        logger.error(f"CustomException occurred: {ce.message}")
        raise HTTPException(status_code=500, 
                            detail=str(CustomException("Failed to get AI response", error_detail=ce)))
    