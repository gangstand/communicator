from pydantic import BaseModel

from domain.typing import EntityRead


class FileRead(EntityRead):
    name: str
    path: str


class FileCreate(BaseModel):
    name: str
    path: str


class FileReposnse(BaseModel):
    name: str
    path: str
    size: int
