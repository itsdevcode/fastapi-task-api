from fastapi.routing import APIRoute
from fastapi import Response
from collections.abc import Callable
from custom_requests.gzip_request import GzipRequest

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # ✅ Original Request → GzipRequest mein convert karo
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler