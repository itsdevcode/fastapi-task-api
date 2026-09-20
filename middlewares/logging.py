from starlette.types import ASGIApp, Scope, Receive, Send

class LoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)  # lifespan/websocket seedha pass karo
            return
   
        path = scope.get("path", "")
        method = scope.get("method", "")
       
     

        async def custom_send(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                print(f"=============> RESPONSE {method} {path} {status_code}")
            
            await send(message)
        
        await self.app(scope, receive, custom_send)

