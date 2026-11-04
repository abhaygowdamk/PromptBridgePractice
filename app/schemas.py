from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password:str=Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password:str=Field(min_length=8, max_length=128)

    
class UserUpdate(BaseModel):
        name: str|None = Field(default=None, min_length=1, max_length=100)
        email:EmailStr|None = None
        
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(validation_alias="username")
    email:EmailStr
    created_at: datetime
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    response: str
    
class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    prompt: str
    llm_response: str = Field(validation_alias="response")
    created_at: datetime