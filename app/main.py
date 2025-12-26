from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import db_helper
from app.routers import email


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    db_helper.init_db()
    yield
    # shutdown
    db_helper.dispose()


app = FastAPI(title="Anti-Mail Microservice", lifespan=lifespan)

app.include_router(email.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
