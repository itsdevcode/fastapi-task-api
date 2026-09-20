from fastapi import FastAPI
from routers.task import task_router
from routers.user import user_router
from middlewares.timing import TimingMiddleware

def create_app() ->FastAPI:
    app = FastAPI(
        title="Tasks API",
        description="Tasks API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    register_middlewares(app)
    register_routers(app)
    return app

def register_middlewares(app: FastAPI) -> None:
    app.add_middleware(TimingMiddleware)

def register_routers(app: FastAPI) -> None:
    api_v1_prefix = "/api/v1"
    app.include_router(user_router, prefix=f"{api_v1_prefix}/users", tags=["Users"])
    app.include_router(task_router, prefix=f"{api_v1_prefix}/tasks", tags=["Tasks"])

app = create_app()

# --- Health Check ---
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.get("/test")
async def test_route():
    user_data = {"id": 1, "name": "Arun", "roles": ["admin"]}
    breakpoint()  # <--- Execution yahan ruk jayegi (Die)
    return {"status": "ok"}