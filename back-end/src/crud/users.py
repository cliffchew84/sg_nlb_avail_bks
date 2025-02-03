from typing import Optional

from supabase import Client

from src.crud.base import CRUDBase
from src.modals.users import (
    User,
    UserCreate,
    UserUpdate,
)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(
        self,
        db: Client,
        *,
        obj_in: UserCreate,
        excludes: Optional[set[str]] = None,
    ) -> User:
        return await super().create(db, obj_in=obj_in, excludes=excludes)

    async def get(self, db: Client, *, i: str) -> User | None:
        return await super().get(db, i=i)

    async def get_all(self, db: Client) -> list[User]:
        return await super().get_all(db)

    async def update(
        self,
        db: Client,
        *,
        obj_in: UserUpdate,
        i: str,
        excludes: Optional[set[str]] = None,
    ) -> User:
        return await super().update(db, obj_in=obj_in, i=i, excludes=excludes)

    async def delete(self, db: Client, *, i: str) -> User | None:
        return await super().delete(db, i=i)


user_crud = CRUDUser(User)
