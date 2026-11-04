from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.models import User, ChatMessage
from app.dependency import get_current_user
from app.llm_service import get_llm_response

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(data: ChatRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):

    answer = await get_llm_response(data.prompt)

    chatmessage = ChatMessage(user_id = current_user.id, prompt = data.prompt, response=answer)

    db.add(chatmessage)
    await db.commit()
    await db.refresh(chatmessage)

    return {"response": answer}
