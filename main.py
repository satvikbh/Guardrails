from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import traceback
import logging
from nemoguardrails import LLMRails, RailsConfig
from langchain_openai import AzureChatOpenAI

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Guardrails API", description="Azure Open AI-based guardrails for detecting jailbreak, toxic input, criticism, and DOR PIL content", version="1.0.0")

# Initialize Azure Open AI model
try:
    logger.info("Initializing Azure Open AI client")
    azure_llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2023-05-15",
        deployment_name="gpt-4o",
        max_tokens=50,  # Match config.yml
        temperature=0.7,
        n=1,
        top_p=0.9
    )
except Exception as e:
    logger.error(f"Azure Open AI initialization failed: {str(e)}")
    logger.error(traceback.format_exc())
    raise

# Initialize NeMo Guardrails
try:
    logger.info("Loading Guardrails configuration")
    rails_config_path = os.path.join(os.getcwd(), "rails_config")
    config = RailsConfig.from_path(rails_config_path)
    logger.info("Initializing LLMRails")
    rails = LLMRails(config=config, llm=azure_llm)
except Exception as e:
    logger.error(f"Guardrails initialization failed: {str(e)}")
    logger.error(traceback.format_exc())
    raise

class GuardrailsRequest(BaseModel):
    user_input: str

class GuardrailsResponse(BaseModel):
    response: str
    is_harmful: bool

@app.post("/guardrails", response_model=GuardrailsResponse)
async def apply_guardrails(data: GuardrailsRequest):
    try:
        logger.debug(f"Received input: {data.user_input}")
        response = await rails.generate_async(prompt=data.user_input)
        logger.debug(f"Guardrails response: {response}")
        
        # Determine if the input is harmful based on the response
        is_harmful = response in [
            "I'm sorry, I can't respond to that request as it appears inappropriate.",
            "I'm sorry, criticism of individuals is not allowed. Please rephrase your request.",
            "I'm sorry, that request related to DOR PIL is not allowed. Please try something else."
        ]
        
        return GuardrailsResponse(
            response=response,
            is_harmful=is_harmful
        )
    except Exception as e:
        logger.error(f"Guardrails processing failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")