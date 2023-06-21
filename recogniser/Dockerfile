FROM tiangolo/uvicorn-gunicorn:python3.9

WORKDIR /recogniser

COPY . ./recogniser

COPY requirements.txt /recogniser/requirements.txt
RUN pip install --upgrade pip
RUN pip install -U pip wheel cmake
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install --no-cache-dir --upgrade -r /recogniser/requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "--bind", ":8080", "recogniser.app:app", "--worker-class", "uvicorn.workers.UvicornH11Worker", "--timeout", "300", "--max-requests", "100", "--backlog", "2048", "--workers", "2", "--threads", "4", "--log-level", "debug"]