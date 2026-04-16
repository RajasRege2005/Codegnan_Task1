import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class ClientCredential(Base):
    __tablename__ = "client_credentials"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    key_hash = Column(String, unique=True, index=True, nullable=False)
    client_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    total_requests = Column(Integer, default=0)
