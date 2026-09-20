from fastapi import FastAPI
from routers.task import task_router
from routers.user import user_router

app = FastAPI(
    title="Tasks API",
    description="Tasks API",
    version="0.1.0",
)

app.include_router(task_router)
app.include_router(user_router)



