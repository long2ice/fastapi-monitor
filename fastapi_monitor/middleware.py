import time

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request


async def monitor(request: Request, call_next: RequestResponseEndpoint):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    status_code = response.status_code
    return response
