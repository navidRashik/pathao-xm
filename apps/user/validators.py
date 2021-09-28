from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    completed: bool


class UserIn(BaseModel):
    first_name: str
    last_name: str
    password: str
