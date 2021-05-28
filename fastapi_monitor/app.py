import os

from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from fastapi_monitor.constants import BASE_DIR
from fastapi_monitor.routes import router


class FastAPIMonitor(FastAPI):
    def configure(self, main_app: FastAPI, path: str = '/monitor'):
        main_app.mount(path + '/api', self)
        directory = os.path.join(BASE_DIR, "static")
        main_app.mount('/assets', StaticFiles(directory=os.path.join(directory, 'assets')), name="static")

        templates = Jinja2Templates(directory=directory)

        @main_app.get(path)
        async def _(request: Request):
            return templates.TemplateResponse('index.html', context={'request': request})


app = FastAPIMonitor()
app.include_router(router)
