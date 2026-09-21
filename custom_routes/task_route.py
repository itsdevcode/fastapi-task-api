from fastapi.routing import APIRoute
from collections.abc import Callable
from fastapi import Request, Response

class TaskRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        orginal_route_handler = super().get_route_handler()
        
        async def custom_route_handler(request: Request) -> Response:
            print(f"=============> Special Processing: {request.method} {request.url.path}")
            body = await request.body()
            print(f"=============> Request Body: {body}")
            return await original_route_handler(request)
            
        return custom_route_handler