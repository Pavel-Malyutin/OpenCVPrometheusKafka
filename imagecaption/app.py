import codecs
import json
import os
import pickle
import time

import cv2
import requests
from kafka import KafkaProducer

imageinput_host = os.environ.get("IMAGEINPUT_HOST", "localhost")
imageinput_port = os.environ.get("IMAGEINPUT_PORT", "8012")
host = os.getenv("KAFKA_HOST", "localhost")
port = os.getenv("KAFKA_PORT", "9092")
kafka_topic = "responses"
imageinput_url = f"http://{imageinput_host}:{imageinput_port}/recognise_array"

producer = KafkaProducer(bootstrap_servers=f"{host}:{port}", security_protocol="PLAINTEXT", api_version=(3, 3))
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        raise Exception("Cant read image from camera")
    img = codecs.encode(pickle.dumps(frame, protocol=pickle.HIGHEST_PROTOCOL), "base64").decode('latin1')
    data = {"img": img}
    try:
        response = requests.post(imageinput_url, json=data)
        user = response.json()
        producer.send(kafka_topic, json.dumps(user).encode("utf-8"))
    except requests.ConnectionError:
        print("Connection error")

    time.sleep(1)

cam.release()
