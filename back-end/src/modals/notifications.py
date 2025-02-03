from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel

from src.modals.base import ResponseBase, CreateBase, UpdateBase


class NotificationBase(BaseModel):
    """Notification Table"""

    id: int
    title: str
    description: str | None
    isRead: bool
    action: str | None
    email: str


class Notification(ResponseBase, NotificationBase):
    table_name: ClassVar[str] = "notifications"
    createdAt: datetime  # Auto populated by database


class NotificationCreate(CreateBase, Notification):
    """Notification model for creating new user-notification relationship"""


class NotificationUpdateBase(BaseModel):
    title: str | None = None
    description: str | None = None
    isRead: bool | None = None
    action: str | None = None
    email: str | None = None


class NotificationUpdate(UpdateBase, NotificationUpdateBase):
    """UserLibrary model for updating user-book relationship"""
