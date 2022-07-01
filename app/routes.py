from fastapi.routing import APIRoute

async def homepage():
    return {"ok":"ok"}

routes = [
    APIRoute("/", endpoint=homepage)
]