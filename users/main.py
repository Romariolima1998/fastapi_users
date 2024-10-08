from fastapi import FastAPI

from users.routers import users


app = FastAPI()

app.include_router(users.router)