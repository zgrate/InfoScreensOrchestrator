FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt && pip install gunicorn

COPY InfosystemOrchestrator /code/

ENTRYPOINT ["gunicorn", "--workers=5", "--threads=2", "--worker-class=gthread", "InfosystemOrchestrator.wsgi:application", "--bind", "0.0.0.0:8000"]
