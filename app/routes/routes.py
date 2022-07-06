from fastapi.routing import APIRoute, Mount
import v1

async def homepage():
    return {"ok":"ok"}

routes = [
    APIRoute('/', endpoint=homepage),
    Mount('/v1', routes=v1.routes),
]