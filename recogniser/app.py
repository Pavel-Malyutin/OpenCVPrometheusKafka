import uvicorn
from fastapi import FastAPI

from recogniser.exceptions import exception_handler
from recogniser.router import router
from recogniser.database.db_setup import db
from recogniser.src import Recogniser

app = FastAPI(title="Face recogniser",
              description="Detect and authorise faces",
              version="0.0.1",
              contact={
                  "name": "Pavel",
                  "email": "test@example.com"}
              )


@app.on_event("startup")
async def shutdown():
    db.init()
    recogniser = Recogniser()
    await recogniser.update_cache()


@app.on_event("shutdown")
async def shutdown():
    await db.close()


app.exception_handler(exception_handler)
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run("app:app", host="localhost", port=8182, reload=True, log_level="debug")
