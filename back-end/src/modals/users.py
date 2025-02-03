from typing import ClassVar, Literal, Optional

from pydantic import BaseModel

from src.modals.base import ResponseBase, CreateBase, UpdateBase


class UserBase(BaseModel):
    """User Mapping Table"""

    """Email"""
    email: str
    username: str | None
    channel_push: bool
    channel_email: bool
    notification_type: Literal["all_notif", "book_updates_only", "no_notif"]


class User(ResponseBase, UserBase):
    table_name: ClassVar[str] = "users"
    pk: ClassVar[str] = "email"


class UserCreate(CreateBase, User):
    """User model for creating new user"""


class UserUpdateBase(BaseModel):
    email: str
    username: str | None
    channel_push: Optional[bool] = None
    channel_email: Optional[bool] = None
    notification_type: Optional[
        Literal["all_notif", "book_updates_only", "no_notif"]
    ] = None


class UserUpdate(UpdateBase, UserUpdateBase):
    """User model for updating user"""
