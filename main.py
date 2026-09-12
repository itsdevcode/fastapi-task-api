from fastapi import FastAPI
from routers.task import task_router

app = FastAPI(
    title="Tasks API",
    description="Tasks API",
    version="0.1.0",
)

app.include_router(task_router)
