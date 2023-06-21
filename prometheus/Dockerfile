FROM tiangolo/uvicorn-gunicorn:python3.9-slim

WORKDIR /prometheus

COPY . ./prometheus

COPY requirements.txt /prometheus/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /prometheus/requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "--bind", ":8080", "prometheus.app:app", "--worker-class", "uvicorn.workers.UvicornH11Worker", "--timeout", "300", "--max-requests", "100", "--backlog", "2048", "--workers", "1", "--threads", "4", "--log-level", "debug"]