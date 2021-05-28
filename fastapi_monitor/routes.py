from fastapi import APIRouter
from starlette.requests import Request


router = APIRouter()


@router.get('/')
async def index(request: Request):
    return {'hello': 'world'}
