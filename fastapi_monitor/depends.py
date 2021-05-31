from starlette.requests import Request


async def monitoring(request: Request):
    request.state.monitor = True
