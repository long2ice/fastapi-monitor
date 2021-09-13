import abc
from email.message import EmailMessage

import aiosmtplib
from starlette.requests import Request
from starlette.responses import Response

from fastapi_monitor.models import RequestLog


class Provider:
    @abc.abstractmethod
    async def send(self, request: Request, response: Response, log: RequestLog):
        pass

    async def handle(self, request: Request, response: Response, log: RequestLog):
        if log.status_code == 500 or log.time > 3:
            await self.send(request, response, log)

    async def get_content(self, request: Request, response: Response, log: RequestLog):
        return f"{log.path} - {log.method} - {log.status_code} - {log.time} - {log.created_at}"


class EmailProvider(Provider):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        msg_from: str,
        msg_to: str,
        msg_subject: str,
        **kwargs,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.kwargs = kwargs
        self.msg_from = msg_from
        self.msg_to = msg_to
        self.msg_subject = msg_subject

    async def send(self, request: Request, response: Response, log: RequestLog):
        message = EmailMessage()
        message["From"] = self.msg_from
        message["To"] = self.msg_to
        message["Subject"] = self.msg_subject
        message.set_content(await self.get_content(request, response, log))
        await aiosmtplib.send(
            message,
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            **self.kwargs,
        )
