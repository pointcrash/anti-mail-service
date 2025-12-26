from typing import List, Union
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import db_helper
from app.schemas import EmailRequest, EmailResponse, EmailStatusResponse
from app.models import EmailModel, EmailStatus
from app.services.email_service import send_email_task

router = APIRouter(prefix="/email", tags=["emails"])

@router.post("/send", response_model=Union[EmailResponse, List[EmailResponse]])
async def send_email(
        request: EmailRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(db_helper.session_getter),
):
    recipients = request.recipient
    is_list = isinstance(recipients, list)
    if not is_list:
        recipients = [recipients]

    created_emails = []
    for recipient in recipients:
        new_email = EmailModel(
            recipient=recipient,
            subject=request.subject,
            body=request.body,
            status=EmailStatus.PENDING
        )
        db.add(new_email)
        created_emails.append(new_email)

    await db.commit()

    responses = []
    for email in created_emails:
        await db.refresh(email)
        background_tasks.add_task(send_email_task, email.id)
        responses.append(EmailResponse(
            id=email.id,
            status=email.status,
            message="Email queued for sending"
        ))

    if not is_list:
        return responses[0]
    return responses

@router.get("/status/{email_id}", response_model=EmailStatusResponse)
async def get_status(email_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    stmt = select(EmailModel).where(EmailModel.id == email_id)
    result = await db.execute(stmt)
    email_obj = result.scalar_one_or_none()

    if not email_obj:
        raise HTTPException(status_code=404, detail="Email not found")

    return email_obj
