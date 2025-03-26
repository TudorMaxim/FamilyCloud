from pydantic import BaseModel


class UserBaseDTO(BaseModel):
    id: int
    email: str
