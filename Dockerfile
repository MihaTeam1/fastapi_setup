FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
COPY dev-requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -r dev-requirements.txt
COPY app ./app/
COPY migrations ./migrations/
COPY alembic.ini ./
COPY pytest.ini ./
COPY gunicorn.config.py .
ENV PYTHONPATH="$PYTHONPATH:/app"

CMD alembic upgrade head