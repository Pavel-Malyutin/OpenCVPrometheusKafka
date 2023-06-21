from fastapi import APIRouter, File, UploadFile
from fastapi.responses import PlainTextResponse, RedirectResponse

from imageinput.models import Face
from imageinput.src import Processor

router = APIRouter()
processor = Processor()


@router.post("/recognise_array")
async def recognise_array(image: Face):
    """
    Add face image in array
    """
    response = processor.recognise_array(data=image.img)
    return response


@router.post("/recognise_jpg")
async def recognise_jpg(file: UploadFile = File(...)):
    """
    Add face image in jpg
    """
    contents = await file.read()
    response = processor.recognise_jpg(data=contents)
    return response


@router.post("/add_face_jpg")
async def add_face_jpg(name: str, file: UploadFile = File(...)):
    """
    Add face image in jpg
    """
    contents = await file.read()
    response = processor.add_face(name=name, data=contents)
    return response


@router.get("/echo", response_class=PlainTextResponse)
async def echo():
    """
    Echo
    """
    return "ok"


@router.get("/")
async def redirect():
    return RedirectResponse("/docs")
