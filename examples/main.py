import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_monitor.app import app as monitor_app

from fastapi_monitor.middleware import monitor

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=monitor)
monitor_app.configure(app)

if __name__ == '__main__':
    uvicorn.run('main:app', debug=True, reload=True)
