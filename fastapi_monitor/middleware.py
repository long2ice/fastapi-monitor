import time

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request

from fastapi_monitor.app import app
from fastapi_monitor.models import Log


async def monitor_middleware(request: Request, call_next: RequestResponseEndpoint):
    start_time = time.time()
    response = await call_next(request)
    monitor = getattr(request.state, "monitor", None)
    if not monitor:
        return response
    process_time = time.time() - start_time
    status_code = response.status_code
    await app.put_log(
        Log(
            path=request.scope["path"],
            method=request.method,
            status_code=status_code,
            time=process_time,
        )
    )
    return response
