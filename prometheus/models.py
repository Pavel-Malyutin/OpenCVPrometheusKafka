from pydantic import BaseModel


class RequestMetric(BaseModel):
    duration: int
    status: str
    endpoint: str


class MethodMetric(BaseModel):
    duration: int
    method: str
