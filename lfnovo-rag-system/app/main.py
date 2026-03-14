from fastapi import FastAPI
from app.api.routes import health, documents, query
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR, tags=["Documents"])
app.include_router(query.router, prefix=settings.API_V1_STR, tags=["Query"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
