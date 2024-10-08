from datetime import datetime
from pydantic import BaseModel



class UserCreateInput(BaseModel):
    username: str
    password: str
    email: str

class UserCreateOutput(BaseModel):
    id: int
    username: str
    password: str
    email: str
    created_at: datetime
    update_at: datetime

    
