from pydantic import BaseModel

from app.schemas.user import UserResponse

class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str