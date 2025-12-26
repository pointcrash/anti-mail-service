import asyncio
import aiosmtplib
from email.message import EmailMessage
from sqlalchemy import select
from app.database import db_helper
from app.models import EmailModel, EmailStatus
from app.config import settings

async def send_email_task(email_id: int):
    async with db_helper.session_factory() as session:
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
                message["From"] = settings.smtp.from_email
                message["To"] = email_obj.recipient
                message["Subject"] = email_obj.subject
                message.set_content(email_obj.body)

                await aiosmtplib.send(
                    message,
                    hostname=settings.smtp.host,
                    port=settings.smtp.port,
                    username=settings.smtp.user,
                    password=settings.smtp.password,
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
