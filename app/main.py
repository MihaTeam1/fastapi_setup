import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path

root = str(Path(__file__).parent.resolve())
if root not in sys.path:
    sys.path.insert(1, root)

from v1 import router as v1_router
from settings import settings

app = FastAPI(
    middleware=settings.middleware,
    exception_handlers=settings.exception_handlers,
)
app.include_router(router=v1_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


