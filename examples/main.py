import asyncio
import random

import uvicorn
from fastapi import Depends, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise

from fastapi_monitor import models
from fastapi_monitor.app import app as monitor_app
from fastapi_monitor.depends import monitoring
from fastapi_monitor.middleware import monitor_middleware

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=monitor_middleware)
monitor_app.configure(app)
register_tortoise(
    app,
    config={
        "connections": {"default": "mysql://root:123456@127.0.0.1:3306/fastapi-monitor"},
        "apps": {"models": {"models": [models]}},
    },
    generate_schemas=True,
)


@app.get("/", dependencies=[Depends(monitoring)])
async def index():
    seconds = random.uniform(0, 1)
    await asyncio.sleep(seconds)
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)
