from fastapi import APIRouter
from fastapi.responses import StreamingResponse, PlainTextResponse, RedirectResponse

from notificator.src import UsersFromKafka

router = APIRouter()


@router.get("/stream")
async def request_handler() -> StreamingResponse:
    """
    Users status stream
    """
    users = UsersFromKafka()
    response = StreamingResponse(
        content=users(),
        media_type="text/html",
    )
    return response


@router.get("/get_users_list")
async def get_users_list() -> list:
    """
    Get all usernames
    """
    users = Users()
    return users.get_users()


@router.get("/get_user_status")
async def get_user_status(user_name: str) -> str:
    """
    Get user status
    """
    users = Users()
    return users.get_user_status(user_name)


@router.get("/echo", response_class=PlainTextResponse)
async def echo():
    """
    Echo
    """
    return "ok"


@router.get("/")
async def redirect():
    return RedirectResponse("/docs")

