from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import models
from database import engine
from routers import auth, resource

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gateway Service",
    description="A FastAPI backend service managing API access credentials and rate limits.",
    version="1.0.0"
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 429:
        return JSONResponse(
            status_code=429,
            content={"error": "RateLimitExceeded", "retry_after": 60, "message": str(exc.detail)},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

app.include_router(auth.router)
app.include_router(resource.router)

@app.get("/")
def root():
    return {"status": "ok", "docs": "Visit /docs for OpenAPI documentation."}
