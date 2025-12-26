from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models import EmailStatus

class EmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    body: str

class EmailResponse(BaseModel):
    id: int
    status: EmailStatus
    message: str

class EmailStatusResponse(BaseModel):
    id: int
    status: EmailStatus
    error_message: Optional[str] = None
    updated_at: datetime
