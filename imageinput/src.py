import codecs
import os
import pickle

import cv2
import numpy as np
import requests


class Processor:
    def __init__(self):
        self.host = os.getenv("RECOGNISER_HOST", "localhost")
        self.port = os.getenv("RECOGNISER_PORT", "8182")
        self.url_add = f"http://{self.host}:{self.port}/add_face"
        self.url_recognise = f"http://{self.host}:{self.port}/recognise"
        self.max_height = 900
        self.max_width = 900

    @staticmethod
    def __decode(data: str) -> np.array:
        return pickle.loads(codecs.decode(data.encode('latin1'), "base64"))

    @staticmethod
    def __encode(data: np.array) -> str:
        return codecs.encode(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL), "base64").decode('latin1')

    def recognise_array(self, data: str) -> dict:
        image_arr = self.__decode(data)
        image = self.__compress_image(image_arr)
        return self.__send_to_recognise(image)

    def recognise_jpg(self, data: bytes) -> dict:
        image_arr = np.fromstring(data, np.uint8)
        img = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
        image = self.__compress_image(img)
        return self.__send_to_recognise(image)

    def add_face(self, data: bytes, name: str) -> dict:
        image_arr = np.fromstring(data, np.uint8)
        img = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
        image = self.__compress_image(img)
        return self.__send_to_add_face(image, name)

    def __compress_image(self, image: np.array) -> np.array:
        height, width = image.shape[:2]
        if self.max_height < height or self.max_width < width:
            scaling_factor = self.max_height / float(height)
            if self.max_width / float(width) < scaling_factor:
                scaling_factor = self.max_width / float(width)
            image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        return image

    def __send_to_recognise(self, image: np.array) -> dict:
        face = self.__encode(image)
        data = {"face": face}
        try:
            response = requests.post(self.url_recognise, json=data)
            print(f"Image sent, status code: {response.status_code}")
            return dict(response.json())
        except requests.ConnectionError:
            return {'status': "Connection error"}

    def __send_to_add_face(self, image: np.array, name: str) -> dict:
        face = self.__encode(image)
        data = {"face": face, "name": name}
        try:
            response = requests.post(self.url_add, json=data)
            print(f"Image sent, status code: {response.status_code}")
            return dict(response.json())
        except requests.ConnectionError:
            return {'status': "Connection error"}
