from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
import schemas
from dependencies import verify_api_key_and_rate_limit
from database import get_db

router = APIRouter(prefix="/api/v1", tags=["Protected Resources"])

@router.get("/data", summary="Get Secure Data", response_description="A protected resource payload")
async def get_secure_data(client: models.ClientCredential = Depends(verify_api_key_and_rate_limit)):
    return {
        "message": "You have successfully accessed the protected resource!",
        "client_name": client.client_name,
        "total_requests": client.total_requests
    }
