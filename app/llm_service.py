import os
from dotenv import load_dotenv
from google import genai
from fastapi import HTTPException, status

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Api key is missing please check the .env file")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"

async def get_llm_response(prompt:str) -> str:
    response = await client.aio.models.generate_content(
        model = MODEL,
        contents = prompt,
    )

    if not response.text:
        raise HTTPException(
            status_code = status.HTTP_502_BAD_GATEWAY,
            detail= "No response from gemini"
        )

    return response.text