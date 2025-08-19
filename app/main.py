from fastapi import FastAPI
from routers import user, role, permission
from config.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def root():
    return "OK"

app.include_router(user.router)
app.include_router(role.router)
app.include_router(permission.router)
