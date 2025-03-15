from functools import lru_cache
from typing import Union

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base
from app.routers import todos
from app import config

# Crear la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(todos.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Asegurar que todas las rutas funcionan correctamente
todos.router.prefix = ""

# Global HTTP exception handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# To use the settings
@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    print(settings.app_name)
    return {"message": "API is running"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
