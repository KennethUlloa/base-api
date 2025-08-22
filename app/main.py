from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.config.lifespan import lifespan
from app.routes import user, role, permission, auth

app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def root():
    return "OK"


app.include_router(user.router)
app.include_router(role.router)
app.include_router(permission.router)
app.include_router(auth.router)
