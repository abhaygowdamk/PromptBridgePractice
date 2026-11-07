from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routes import auth, users, chat
from app.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="PromptBridge", lifespan=lifespan)

# Register exception handlers
register_exception_handlers(app)

# Register API routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"message": "Welcome to PromptBridge API"}
