import uvicorn
from fastapi import FastAPI
from routes import routes
from settings import settings

import sys

app = FastAPI(routes=routes, **settings)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


