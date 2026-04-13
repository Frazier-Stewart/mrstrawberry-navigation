import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import engine, Base
from app.routers import auth, categories, bookmarks, export_import

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Navigation Site API", version="1.0.0")

_cors_origins_env = os.getenv("CORS_ORIGINS", "")
_default_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
allow_origins = (
    [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
    if _cors_origins_env
    else _default_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(bookmarks.router)
app.include_router(export_import.router)


@app.get("/health")
def health():
    return {"status": "ok"}
