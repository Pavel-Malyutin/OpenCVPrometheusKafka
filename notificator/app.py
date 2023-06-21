import uvicorn
from fastapi import FastAPI

from notificator.exceptions import exception_handler
from notificator.routers import router

app = FastAPI(title="Users info",
              description="Get info about users",
              version="0.0.1",
              contact={
                  "name": "Pavel",
                  "email": "test@example.com"}
              )

app.include_router(router)
app.exception_handler(exception_handler)

if __name__ == '__main__':
    uvicorn.run("app:app", host="localhost", port=8011, reload=True, log_level="debug")
