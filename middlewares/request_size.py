from starlette.types import ASGIApp, Scope, Receive, Send

class RequestSizeMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
    
    async def __call__(self,scope:Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        path = scope["path"]
        method = scope["method"]

        total_bytes = 0 

        async def custom_receive():
            nonlocal total_bytes
            message = await receive()
            if message["type"] == "http.request":
                chunk = message.get("body",b"")
                
                total_bytes += len(chunk)
                more_body = message.get("more_body",False)
                if not more_body:
                    print(f"=============> REQUEST {method} {path} | Total Bytes: {total_bytes}")

            return message

        await self.app(scope, custom_receive, send)