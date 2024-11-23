from datetime import datetime
from pydantic import BaseModel, ConfigDict



class UserCreateInput(BaseModel):
    username: str
    password: str
    email: str

class UserCreateOutput(BaseModel):
    id: int
    username: str
    email: str
    # created_at: datetime
    # update_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdateInput(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None


class TokenOutput(BaseModel):
    access_token: str
    token_type: str

class RevokedTokenInput(BaseModel):
    token: str

class MessageOutput(BaseModel):
    message: str


class PasswordRecoveryInput(BaseModel):
    email: str

    
