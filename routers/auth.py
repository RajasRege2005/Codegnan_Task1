from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import security

router = APIRouter(prefix="/credentials", tags=["Credentials"])

@router.post("/", response_model=schemas.CredentialResponse, status_code=status.HTTP_201_CREATED, summary="Obtain Access Credentials")
def create_credential(item: schemas.CredentialCreate, db: Session = Depends(get_db)):
    raw_key = security.generate_api_key()
    key_hash = security.hash_api_key(raw_key)

    if db.query(models.ClientCredential).filter(models.ClientCredential.key_hash == key_hash).first():
        raise HTTPException(status_code=400, detail="Key generation collision. Please try again.")

    db_credential = models.ClientCredential(
        client_name=item.client_name,
        key_hash=key_hash
    )
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)

    return schemas.CredentialResponse(
        client_name=db_credential.client_name,
        api_key=raw_key,
        created_at=db_credential.created_at
    )
