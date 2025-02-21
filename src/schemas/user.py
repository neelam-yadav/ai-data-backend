from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    pipelines: Optional[List["Pipeline"]] = []

    class Config:
        orm_mode = True


class UserResponseLite(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
