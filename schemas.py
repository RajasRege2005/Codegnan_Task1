from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CredentialCreate(BaseModel):
    client_name: str

class CredentialResponse(BaseModel):
    client_name: str
    api_key: str  
    created_at: datetime

class UsageResponse(BaseModel):
    client_name: str
    total_requests: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
