import asyncio
from typing import List

from fastapi import FastAPI

from fastapi_monitor.models import RequestLog
from fastapi_monitor.notifications import Provider
from fastapi_monitor.routes import router


class FastAPIMonitor(FastAPI):
    bulk_size: int = 10
    max_seconds: int = 60
    queue: asyncio.Queue
    logs: List[RequestLog] = []
    lock: asyncio.Lock
    notifications: List[Provider]

    async def put_log(self, log: RequestLog):
        await self.queue.put(log)

    async def consume(self):
        while True:
            timeout = False
            try:
                log = await asyncio.wait_for(self.queue.get(), self.max_seconds)
                self.logs.append(log)
            except asyncio.TimeoutError:
                timeout = True
            async with self.lock:
                if len(self.logs) == self.bulk_size or (self.logs and timeout):
                    await RequestLog.bulk_create(self.logs)
                    self.logs = []

    def configure(
        self,
        main_app: FastAPI,
        path: str = "/monitor",
        bulk_size: int = 10,
        max_seconds: int = 60,
        notifications: List[Provider] = None,
    ):
        """
        Configure FastAPIMonitor
        :param notifications:
        :param path: mount path
        :param max_seconds: Log create max seconds
        :param bulk_size: async bulk_size to create log
        :param main_app:
        :return:
        """
        self.bulk_size = bulk_size
        self.max_seconds = max_seconds
        self.queue = asyncio.Queue()
        self.lock = asyncio.Lock()
        self.notifications = notifications or []
        main_app.mount(path, self)

        @main_app.on_event("startup")
        async def startup():
            asyncio.ensure_future(self.consume())

        @main_app.on_event("shutdown")
        async def shutdown():
            if self.logs:
                await RequestLog.bulk_create(self.logs)
                self.logs = []


app = FastAPIMonitor()
app.include_router(router)
