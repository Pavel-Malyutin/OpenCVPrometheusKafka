from pydantic import BaseModel


class User(BaseModel):
    face: str
    name: str


class UnknownUser(BaseModel):
    face: str

