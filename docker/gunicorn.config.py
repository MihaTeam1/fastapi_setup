from pathlib import Path
pythonpath = str(Path(__file__).parent) + '/app'
bind = '0.0.0.0:8000'
worker_class = 'uvicorn.workers.UvicornWorker'
workers = 3
limit_request_fields = 32000
limit_request_fields_size = 0