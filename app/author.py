from pydantic import BaseModel

class CreateAuthor(BaseModel):
    nickname: str
    genre: str

class Author:
    def __init__(self, id: int, nickname: str, genre: str) -> None:
        self.id = id
        self.nickname = nickname
        self.genre = genre