FROM tiangolo/uvicorn-gunicorn:python3.9-slim

WORKDIR /notificator

COPY . ./notificator

COPY requirements.txt /notificator/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /notificator/requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "--bind", ":8080", "notificator.app:app", "--worker-class", "uvicorn.workers.UvicornH11Worker", "--timeout", "300", "--max-requests", "100", "--backlog", "2048", "--workers", "2", "--threads", "4", "--log-level", "debug"]