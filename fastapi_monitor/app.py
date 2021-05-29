import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from fastapi_monitor.constants import BASE_DIR
from fastapi_monitor.routes import router


class FastAPIMonitor(FastAPI):
    def configure(self, main_app: FastAPI):
        main_app.mount('/monitor/api', self)
        main_app.mount('/monitor', StaticFiles(directory=os.path.join(BASE_DIR, "web"), html=True), name="web")


app = FastAPIMonitor()
app.include_router(router)
