from starlette.types import ASGIApp, Scope, Receive, Send

class ResponseSizeMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) ->None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        path = scope.get("path", "")
        method = scope.get("method", "")
        total_bytes = 0

        async def custom_send(message):
            nonlocal total_bytes
            if message["type"] == "http.response.body":
                chunk = message.get("body",b"")
                total_bytes += len(chunk)
                more_body = message.get("more_body", False)
                if not more_body:
                    print(f"=============> Response {method} {path} | Total Bytes: {total_bytes}")

            await send(message)

        await self.app(scope, receive, custom_send)