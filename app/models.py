from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func, ForeignKey, Text
from datetime import datetime



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    created_at:Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    
    
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    
    response: Mapped[str] = mapped_column(Text, nullable=False)
    
    created_at:Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )