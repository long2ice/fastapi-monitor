from starlette.requests import Request


async def enable_monitor(request: Request):
    request.state.monitor = True
