from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8, max_length=120)

class UpdateUser(BaseModel):
    username: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    password: str | None = Field(default=None, max_length=120)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
