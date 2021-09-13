from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise

from examples.settings import settings
from fastapi_monitor import models
from fastapi_monitor.app import app as monitor_app
from fastapi_monitor.middlewares import monitor_middleware
from fastapi_monitor.notifications import EmailProvider


def create_app():
    app = FastAPI()
    app.add_middleware(BaseHTTPMiddleware, dispatch=monitor_middleware)
    monitor_app.configure(
        app,
        notifications=[
            EmailProvider(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_USERNAME,
                password=settings.EMAIL_PASSWORD,
                msg_from=settings.EMAIL_USERNAME,
                msg_to="long2ice@gmail.com",
                msg_subject="Notification from fastapi-monitor",
            )
        ],
    )
    register_tortoise(
        app,
        config={
            "connections": {"default": "mysql://root:123456@127.0.0.1:3306/fastapi-monitor"},
            "apps": {"models": {"models": [models]}},
        },
        generate_schemas=True,
    )
    return app
