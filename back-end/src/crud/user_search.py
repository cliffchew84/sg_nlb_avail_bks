from typing import Optional

from supabase import Client

from src.crud.base import CRUDBase
from src.modals.user_search import (
    UserSearch,
    UserSearchCreate,
    UserSearchUpdate,
)


class CRUDUserSearch(CRUDBase[UserSearch, UserSearchCreate, UserSearchUpdate]):
    async def create(
        self,
        db: Client,
        *,
        obj_in: UserSearchCreate,
        excludes: Optional[set[str]] = None,
    ) -> UserSearch:
        return await super().create(db, obj_in=obj_in, excludes=excludes)

    async def get(self, db: Client, *, i: str) -> UserSearch | None:
        return await super().get(db, i=i)

    async def get_all(self, db: Client) -> list[UserSearch]:
        return await super().get_all(db)

    async def get_multi_by_owner(self, db: Client, *, email: str) -> list[UserSearch]:
        response = (
            db.table(self.model.table_name)
            .select("*, user_books(email)")
            .eq("email", email)
            .execute()
        )
        return [self.model(**item) for item in response.data]

    async def update(
        self,
        db: Client,
        *,
        obj_in: UserSearchUpdate,
        i: str,
        excludes: Optional[set[str]] = None,
    ) -> UserSearch:
        return await super().update(db, obj_in=obj_in, i=i, excludes=excludes)

    async def delete(self, db: Client, *, i: str) -> UserSearch | None:
        return await super().delete(db, i=i)


user_search_crud = CRUDUserSearch(UserSearch)
