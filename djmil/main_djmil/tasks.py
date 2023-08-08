import asyncio
from djmil.celery import app
from .SkySafeApi import make_api_call

@app.task
def start_task():
    loop = asyncio.get_event_loop()
    task = loop.create_task(make_api_call())
    loop.run_until_complete(task)
    loop.run_forever()
