from typing import ClassVar

from pydantic import BaseModel

from src.modals.base import ResponseBase, CreateBase, UpdateBase


class UserLibraryBase(BaseModel):
    """User Librarys Mapping Table"""

    """Email Address"""
    email: str

    """Library name"""
    library_name: str


class UserLibrary(ResponseBase, UserLibraryBase):
    table_name: ClassVar[str] = "user_libraries"


class UserLibraryCreate(CreateBase, UserLibrary):
    """UserLibrary model for creating new user-book relationship"""


class UserLibraryUpdateBase(BaseModel):
    email: str
    library_name: str


class UserLibraryUpdate(UpdateBase, UserLibraryUpdateBase):
    """UserLibrary model for updating user-book relationship"""
