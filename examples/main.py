import asyncio
import random

import uvicorn
from fastapi import Depends

from examples import create_app
from fastapi_monitor.depends import monitoring

app = create_app()


@app.get("/", dependencies=[Depends(monitoring)])
async def index():
    seconds = random.uniform(0, 1)
    await asyncio.sleep(seconds)
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)
