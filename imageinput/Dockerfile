FROM tiangolo/uwsgi-nginx:python3.9

WORKDIR /imageinput

COPY . ./imageinput

COPY requirements.txt /imageinput/requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install --no-cache-dir --upgrade -r /imageinput/requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "--bind", ":8080", "imageinput.app:app", "--worker-class", "uvicorn.workers.UvicornH11Worker", "--timeout", "300", "--max-requests", "100", "--backlog", "2048", "--workers", "2", "--threads", "4", "--log-level", "debug"]