from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteException)
    def http_exception(request, exc):
        return JSONResponse(
            status_code = exc.status_code,
            content = {"message":exc.detail}
        )