import uvicorn

from app.config import settings

if __name__ == "__main__":
    host = "127.0.0.1" if settings.env == "prod" else "0.0.0.0"
    uvicorn.run(
        "app.main:app",
        host=host,
        port=8000,
        reload=settings.env == "dev",
    )
