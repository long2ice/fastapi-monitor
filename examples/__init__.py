from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise

from fastapi_monitor import models
from fastapi_monitor.app import app as monitor_app
from fastapi_monitor.middleware import monitor_middleware


def create_app():
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
    return app
