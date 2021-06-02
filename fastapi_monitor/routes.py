from fastapi import APIRouter
from starlette.requests import Request

from fastapi_monitor.models import Log
from fastapi_monitor.template import templates

router = APIRouter()


@router.get("/")
async def monitor(request: Request):
    return templates.TemplateResponse("dashboard.html", context={"request": request})


@router.get("/logs")
async def logs_page(request: Request):
    return templates.TemplateResponse("logs.html", context={"request": request})


@router.get("/logs/data")
async def logs_data(request: Request, limit: int, offset: int):
    total = await Log.all().count()
    data = await Log.all().limit(limit).offset(offset)
    return {'total': total, 'rows': data}
