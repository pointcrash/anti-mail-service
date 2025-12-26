import asyncio
import aiosmtplib
from email.message import EmailMessage
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import EmailModel, EmailStatus
from app.config import settings

async def send_email_task(email_id: int):
    async with AsyncSessionLocal() as session:
        # Fetch email
        stmt = select(EmailModel).where(EmailModel.id == email_id)
        result = await session.execute(stmt)
        email_obj = result.scalar_one_or_none()
        
        if not email_obj:
            return

        email_obj.status = EmailStatus.PROCESSING
        await session.commit()

        try:
            if settings.USE_REAL_SMTP:
                message = EmailMessage()
                message["From"] = settings.SMTP_FROM_EMAIL
                message["To"] = email_obj.recipient
                message["Subject"] = email_obj.subject
                message.set_content(email_obj.body)

                await aiosmtplib.send(
                    message,
                    hostname=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    username=settings.SMTP_USER,
                    password=settings.SMTP_PASSWORD,
                    start_tls=True
                )
            else:
                # Simulate delay and success
                await asyncio.sleep(10)
                print(f"SIMULATION: Email sent to {email_obj.recipient} with subject '{email_obj.subject}'")

            email_obj.status = EmailStatus.SENT
        except Exception as e:
            email_obj.status = EmailStatus.FAILED
            email_obj.error_message = str(e)
            print(f"ERROR: Failed to send email {email_id}: {e}")
        finally:
            await session.commit()
