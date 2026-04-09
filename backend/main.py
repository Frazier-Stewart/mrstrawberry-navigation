from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import engine, Base
from app.routers import auth, categories, bookmarks

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Navigation Site API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(bookmarks.router)


@app.get("/health")
def health():
    return {"status": "ok"}
