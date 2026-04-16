import os
from fastapi import Request, Depends, HTTPException, status, BackgroundTasks
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
import time
import models
from database import get_db
from security import hash_api_key

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

_in_memory_rate_cache = {}

RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW_SEC = 60

async def verify_api_key_and_rate_limit(
    request: Request, 
    background_tasks: BackgroundTasks,
    api_key: str = Depends(api_key_header), 
    db: Session = Depends(get_db)
) -> models.ClientCredential:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key in headers (X-API-Key)."
        )

    key_hash = hash_api_key(api_key)
    
    client_cred = db.query(models.ClientCredential).filter(models.ClientCredential.key_hash == key_hash).first()
    if not client_cred:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key.")
    
    current_time = time.time()
    current_window = int(current_time // RATE_LIMIT_WINDOW_SEC)
    
    cache_key = f"{key_hash}:{current_window}"
    
    if cache_key not in _in_memory_rate_cache:
        old_keys = [k for k in _in_memory_rate_cache if not k.endswith(f":{current_window}")]
        for k in old_keys:
            del _in_memory_rate_cache[k]
            
        _in_memory_rate_cache[cache_key] = 1
    else:
        _in_memory_rate_cache[cache_key] += 1
        
    if _in_memory_rate_cache[cache_key] > RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum of {RATE_LIMIT_REQUESTS} requests allowed per {RATE_LIMIT_WINDOW_SEC} seconds."
        )

    background_tasks.add_task(increment_usage, client_cred.id)
    return client_cred

def increment_usage(credential_id: str):
    db = next(get_db())
    db.query(models.ClientCredential).filter(models.ClientCredential.id == credential_id).update(
        {models.ClientCredential.total_requests: models.ClientCredential.total_requests + 1}
    )
    db.commit()
    db.close()
