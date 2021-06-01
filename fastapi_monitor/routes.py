from fastapi import APIRouter
from starlette.requests import Request

from fastapi_monitor.models import Log
from fastapi_monitor.template import templates

router = APIRouter()


@router.get("/")
async def monitor(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@router.get("/logs")
async def logs(request: Request):
    data = await Log.all()
    return templates.TemplateResponse("index.html", context={"request": request, 'logs': data})
