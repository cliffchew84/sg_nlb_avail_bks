from typing import Optional

from supabase import Client

from src.crud.base import CRUDBase
from src.modals.notifications import (
    Notification,
    NotificationCreate,
    NotificationUpdate,
)


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    async def create(
        self,
        db: Client,
        *,
        obj_in: NotificationCreate,
        excludes: Optional[set[str]] = None,
    ) -> Notification:
        return await super().create(db, obj_in=obj_in, excludes=excludes)

    async def get(self, db: Client, *, i: str) -> Notification | None:
        return await super().get(db, i=i)

    async def get_all(self, db: Client) -> list[Notification]:
        return await super().get_all(db)

    async def get_multi_by_owner(self, db: Client, *, email: str) -> list[Notification]:
        response = (
            db.table(self.model.table_name)
            .select("*")
            .eq("email", email)
            .order("createdAt", desc=True)
            .limit(25)
            .execute()
        )
        return [self.model(**item) for item in response.data]

    async def update(
        self,
        db: Client,
        *,
        obj_in: NotificationUpdate,
        i: str,
        excludes: Optional[set[str]] = None,
    ) -> Notification:
        return await super().update(db, obj_in=obj_in, i=i, excludes=excludes)

    async def delete(self, db: Client, *, i: str) -> Notification | None:
        return await super().delete(db, i=i)


notification_crud = CRUDNotification(Notification)
