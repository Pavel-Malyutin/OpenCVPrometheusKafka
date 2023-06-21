from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from recogniser.models import User, UnknownUser
from recogniser.src import Recogniser

router = APIRouter()
recogniser = Recogniser()


@router.post("/add_face")
async def add_face(new_user: User) -> dict:
    """
    Add new face to database
    """
    return await recogniser.add_face(image=new_user.face, name=new_user.name)


@router.post("/recognise")
async def recognise(user: UnknownUser) -> dict:
    """
    Recognise face
    """
    return await recogniser.recognize_faces(image=user.face)


@router.get("/health", status_code=201)
async def echo():
    """
    Echo
    """
    return "ok"


@router.get("/")
async def redirect():
    return RedirectResponse("/docs")
