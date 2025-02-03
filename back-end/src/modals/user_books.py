from typing import ClassVar

from pydantic import BaseModel

from src.modals.base import ResponseBase, CreateBase, UpdateBase


class UserBookBase(BaseModel):
    """User Books Mapping Table"""

    """Email Address"""
    email: str

    """Book Reference Number (BRN)"""

    BID: int


class UserBook(ResponseBase, UserBookBase):
    table_name: ClassVar[str] = "user_books"


class UserBookCreate(CreateBase, UserBook):
    """UserBook model for creating new user-book relationship"""


class UserBookUpdateBase(BaseModel):
    BID: int
    email: str


class UserBookUpdate(UpdateBase, UserBookUpdateBase):
    """UserBook model for updating user-book relationship"""
