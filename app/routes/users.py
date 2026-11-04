from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import ChatMessageResponse, UserCreate, UserResponse, UserUpdate
from app.models import ChatMessage, User
from app.security import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.dependency import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession=Depends(get_db)):
    user = User(username=data.name, email=data.email, hashed_password=hash_password(data.password))
    db.add(user)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email already registered"
        )

    await db.refresh(user)
    return user

@router.patch("/update", response_model=UserResponse)
async def update_user(data: UserUpdate, db: AsyncSession=Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if data.name is not None:
        current_user.username = data.name
    if data.email is not None:
        current_user.email = data.email

    await db.commit()
    await db.refresh(current_user)

    return current_user

@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/chat-history", response_model=list[ChatMessageResponse])
async def get_chat_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc())
    )

    return result.scalars().all()

@router.delete("/delete")
async def delete_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Delete the user's chat history first
    await db.execute(
        delete(ChatMessage).where(
            ChatMessage.user_id == current_user.id
        )
    )

    # Delete the user account
    await db.delete(current_user)
    await db.commit()

    return {"message": "User account deleted successfully"}
