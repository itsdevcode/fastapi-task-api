from starlette.types import ASGIApp, Scope, Receive, Send
import time 

class TimingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        #bypass the scoket & lifespan events
        if scope["type"] != "http":
            await self.app(scope,receive, send)
            return
        start_time = time.perf_counter()
        async def custom_send(message):
            if message["type"] == "http.response.start":
                process_time = f"=============> {time.perf_counter() - start_time:.4f}"
                headers = list(message.get("headers", []))
                headers.append((b"x-process-time", process_time.encode("latin-1")))
                message["headers"] = headers
            await send(message)
        await self.app(scope, receive, custom_send)