from fastapi import FastAPI

from users.routers import users
from users.routers import token


app = FastAPI()

app.include_router(users.router)
app.include_router(token.router) 