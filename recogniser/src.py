import codecs
import pickle
from collections import Counter

import face_recognition
import numpy as np
from sqlalchemy.exc import IntegrityError

from recogniser.database.models import UserDB
from recogniser.logger import Logger


class Recogniser:
    logger = Logger()

    def __init__(self, model_type: str = "hog"):
        """
        :param model_type: CNN (convolutional neural network) / HOG (histogram of oriented gradients)
        """
        self.model_type = model_type
        self.cache = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Recogniser, cls).__new__(cls)
        return cls.instance

    @staticmethod
    @logger.log_method_duration
    def decode(data: str) -> np.array:
        return pickle.loads(codecs.decode(data.encode('latin1'), "base64"))

    @staticmethod
    @logger.log_method_duration
    def encode(data: np.array) -> str:
        return codecs.encode(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL), "base64").decode('latin1')

    @logger.log_async_method_duration
    async def update_cache(self):
        users = await UserDB.get_all()
        self.cache = {user.name: self.decode(user.face) for user in users}

    @logger.log_async_method_duration
    async def add_face(self, image: str, name: str) -> dict:
        status = {"user": name, "status": ""}
        try:
            arr = self.decode(image)
        except:
            status["status"] = "Decode error"
            return status
        face_locations = face_recognition.face_locations(arr, model=self.model_type)
        face_encodings = face_recognition.face_encodings(arr, face_locations)
        if len(face_encodings) > 1:
            status["status"] = "More then one face in image"
            return status
        if len(face_encodings) == 0:
            status["status"] = "No face found"
            return status
        face = face_encodings.pop()
        user = {"name": name, "face": self.encode(face)}
        try:
            await UserDB.create(**user)
        except IntegrityError:
            status["status"] = "User already exist"
            return status
        except Exception as e:
            status["status"] = "Error in save to DB"
            return status
        self.cache.update({user["name"]: face})
        status["status"] = "User created"
        return status

    @logger.log_method_duration
    def _recognize_face(self, unknown_encoding: dict) -> str:
        faces = list(self.cache.values())
        names = list(self.cache.keys())
        boolean_matches = face_recognition.compare_faces(faces, unknown_encoding)
        votes = Counter(
            name
            for match, name in zip(boolean_matches, names)
            if match
        )
        if votes:
            return votes.most_common(1)[0][0]
        return "Unknown"

    @logger.log_async_method_duration
    async def recognize_faces(self, image: str) -> dict:
        input_image = self.decode(image)
        input_face_locations = face_recognition.face_locations(input_image, model=self.model_type)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

        for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
            name = self._recognize_face(unknown_encoding)
            if name == "Unknown":
                await self.update_cache()
                name = self._recognize_face(unknown_encoding)
            return {"name": name, "bounding_box": bounding_box}
