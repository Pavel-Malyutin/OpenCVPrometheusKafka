from pydantic import BaseModel


class Face(BaseModel):
    img: str
