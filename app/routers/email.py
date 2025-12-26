from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import db_helper
from app.schemas import EmailRequest, EmailResponse, EmailStatusResponse
from app.models import EmailModel, EmailStatus
from app.services.email_service import send_email_task

router = APIRouter(prefix="/email", tags=["emails"])

@router.post("/send", response_model=EmailResponse)
async def send_email(
        request: EmailRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    # Create DB entry
    new_email = EmailModel(
        recipient=request.recipient,
        subject=request.subject,
        body=request.body,
        status=EmailStatus.PENDING
    )
    db.add(new_email)
    await db.commit()
    await db.refresh(new_email)

    # Add background task
    background_tasks.add_task(send_email_task, new_email.id)

    return EmailResponse(
        id=new_email.id,
        status=new_email.status,
        message="Email queued for sending"
    )

@router.get("/status/{email_id}", response_model=EmailStatusResponse)
async def get_status(email_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    stmt = select(EmailModel).where(EmailModel.id == email_id)
    result = await db.execute(stmt)
    email_obj = result.scalar_one_or_none()

    if not email_obj:
        raise HTTPException(status_code=404, detail="Email not found")

    return email_obj
