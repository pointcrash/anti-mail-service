from fastapi import FastAPI
from app.database import init_db
from app.routers import email

app = FastAPI(title="Anti-Mail Microservice")

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(email.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
