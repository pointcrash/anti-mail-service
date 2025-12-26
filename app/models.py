from enum import Enum
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class EmailStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"

class EmailModel(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipient: Mapped[str]
    subject: Mapped[str]
    body: Mapped[str]
    status: Mapped[EmailStatus] = mapped_column(default=EmailStatus.PENDING)
    error_message: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
