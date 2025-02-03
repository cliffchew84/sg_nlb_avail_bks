from typing import ClassVar, Optional

from pydantic import BaseModel

from src.modals.base import ResponseBase, CreateBase, UpdateBase


class UserSearchBase(BaseModel):
    """User Search Table"""

    """Email (PK)"""
    email: str

    """Database insert time (milliseconds after utc)"""
    search_time: int

    """Search title"""
    Title: Optional[str]

    """Search author"""
    Author: Optional[str]


class UserSearch(ResponseBase, UserSearchBase):
    table_name: ClassVar[str] = "user_search"
    pk: ClassVar[str] = "email"


class UserSearchCreate(CreateBase, UserSearch):
    """UserSearch model for creating new user-book relationship"""


class UserSearchUpdate(UpdateBase, UserSearchBase):
    """UserSearch model for updating user-book relationship"""
