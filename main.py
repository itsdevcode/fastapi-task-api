from fastapi import FastAPI
from routers.task import task_router
from routers.user import user_router
from middlewares.timing import TimingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from middlewares.logging import LoggingMiddleware
from middlewares.response_size import ResponseSizeMiddleware
from middlewares.request_size import RequestSizeMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from fastapi.responses import StreamingResponse
from collections.abc import AsyncIterable

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
    origins = [
        "http://localhost:3000",
    ]
    app.add_middleware(TimingMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestSizeMiddleware)
    app.add_middleware(ResponseSizeMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost","127.0.0.1"], www_redirect=False)
    app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)
    # app.add_middleware(HTTPSRedirectMiddleware,)
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def register_routers(app: FastAPI) -> None:
    api_v1_prefix = "/api/v1"
    app.include_router(user_router, prefix=f"{api_v1_prefix}/users", tags=["Users"])
    app.include_router(task_router,  tags=["Tasks"])

app = create_app()

# --- Health Check ---
@app.get("/health", tags=["Health"])
async def health_check():
    return {"data": "A" * 5000}

@app.get("/test")
async def test_route():
    user_data = {"id": 1, "name": "Arun", "roles": ["admin"]}
    # breakpoint()  # <--- Execution yahan ruk jayegi (Die)
    return {"data": "A" * 5000}

@app.get("/stream-test", response_class=StreamingResponse)
async def stream_test() -> AsyncIterable[bytes]:
    yield b"Hello "    # chunk-1
    yield b"Arun "     # chunk-2
    yield b"Backend"   # chunk-3