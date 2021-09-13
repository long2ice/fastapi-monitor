import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import PositiveInt
from tortoise import timezone

from fastapi_monitor.models import Log

router = APIRouter()


@router.get("/log")
async def logs_data(
    page: PositiveInt,
    size: PositiveInt,
    path: Optional[str] = None,
    status_code: Optional[int] = None,
    method: Optional[str] = None,
    start_time: Optional[datetime.datetime] = None,
    end_time: Optional[datetime.datetime] = None,
):
    limit = size
    offset = (page - 1) * size
    qs = Log.all()
    if path:
        qs = qs.filter(path=path)
    if status_code:
        qs = qs.filter(status_code=status_code)
    if method:
        qs = qs.filter(method=method)
    if start_time and end_time:
        qs = qs.filter(created_at__range=(start_time, end_time))
    else:
        qs = qs.filter(created_at__gte=timezone.now() - datetime.timedelta(days=7))
    total = await qs.count()
    data = await qs.limit(limit).offset(offset)
    return {"total": total, "data": data}
