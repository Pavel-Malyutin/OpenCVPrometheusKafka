FROM python:3.8

WORKDIR /imagecaption

COPY . ./imagecaption

COPY requirements.txt /imagecaption/requirements.txt
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install --no-cache-dir --upgrade -r /imagecaption/requirements.txt

ENV PYTHONUNBUFFERED 1

CMD [ "python", "imagecaption/app.py" ]