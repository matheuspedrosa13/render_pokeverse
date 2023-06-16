from pydantic import BaseModel


class User(BaseModel):
    id_user: str
    name_user: str
    age_user: int
    gender: str
    email: str
    password: str
    status: bool


