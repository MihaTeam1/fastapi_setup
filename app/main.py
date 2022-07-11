import uvicorn
from fastapi import FastAPI
import v1
from settings import settings

app = FastAPI(**settings)
app.include_router(router=v1.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


