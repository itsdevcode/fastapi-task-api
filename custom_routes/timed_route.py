from fastapi.routing import APIRoute
from collections.abc import Callable
from fastapi import Request, Response
import time

class TaskTimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                start_time = time.perf_counter()
                print(f"START TIME: ========>CUSTOM R {start_time}")
                response = await original_route_handler(request)
                return response
            finally:
                duration = (time.perf_counter() - start_time) * 1000
                print(f"DURATION: {duration:.2f} ms")
            
            
        return custom_route_handler