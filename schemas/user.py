from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: Optional[int]
    email: str

    class Config:
        from_attributes = True

class FriendRequest(BaseModel):
    id: Optional[int]
    from_user_id: int
    to_user_id: int
    status: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class FriendRequestCreate(BaseModel):
    to_user_id: int

class FriendRequestResponse(BaseModel):
    friend_request_id: int
    action: str
