"""
main.py
=======
Application entry point.

RUN THE SERVER:
    uvicorn app.main:app --reload

Then open in your browser:
    http://127.0.0.1:8000/docs    -> interactive Swagger UI (try every endpoint here)
    http://127.0.0.1:8000/redoc   -> alternative ReDoc documentation
"""

from dotenv import load_dotenv

# Load variables from .env (e.g. ADMIN_API_KEY) BEFORE other modules
# that read environment variables (like app.auth) are imported.
load_dotenv()

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import header, hero, faq, footer

# Create all database tables on startup if they don't already exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Website Content Management API",
    description=(
        "Dynamic content management API for a website's "
        "Header, Hero Section, FAQ, and Footer."
    ),
    version="1.0.0",
)

# Register each section's router
app.include_router(header.router)
app.include_router(hero.router)
app.include_router(faq.router)
app.include_router(footer.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Website Content Management API is running.",
        "docs": "/docs",
    }