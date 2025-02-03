from typing import Optional

from supabase import Client

from src.crud.base import CRUDBase
from src.modals.users import User
from src.modals.library import (
    Library,
    LibraryCreate,
    LibraryUpdate,
)
from src.modals.user_library import UserLibrary, UserLibraryCreate


class CRUDLibrary(
    CRUDBase[
        Library,
        LibraryCreate,
        LibraryUpdate,
    ]
):
    async def create(
        self,
        db: Client,
        *,
        obj_in: LibraryCreate,
        excludes: Optional[set[str]] = None,
    ) -> Library:
        return await super().create(db, obj_in=obj_in, excludes=excludes)

    async def create_owner(
        self,
        db: Client,
        name: str,
        email: str,
    ) -> None:
        # Add user book relationship table
        user_book = UserLibraryCreate(email=email, library_name=name)
        db.table(UserLibrary.table_name).insert(user_book.model_dump()).execute()
        return

    async def get(self, db: Client, *, i: str) -> Library | None:
        return await super().get(db, i=i)

    async def get_all(self, db: Client) -> list[Library]:
        return await super().get_all(db)

    async def get_multi_by_owner(self, db: Client, *, email: str) -> list[Library]:
        response = (
            db.table("user_libraries")
            .select(f"*, {self.model.table_name}(*)")
            .eq("email", email)
            .execute()
        )
        return [
            Library(**item[self.model.table_name])
            for item in response.data
            if self.model.table_name in item
        ]

    async def get_owners(self, db: Client, *, i: str) -> list[User]:
        """Get users that owns the given library name"""
        response = (
            db.table("user_books")
            .select(f"*, {User.table_name}(*)")
            .eq("library_name", i)
            .execute()
        )
        return [
            User(**item[User.table_name])
            for item in response.data
            if User.table_name in item
        ]

    async def update(
        self,
        db: Client,
        *,
        obj_in: LibraryUpdate,
        i: str,
        excludes: Optional[set[str]] = None,
    ) -> Library:
        return await super().update(db, obj_in=obj_in, i=i, excludes=excludes)

    async def delete_owner(self, db: Client, *, i: str, email: str):
        (
            db.table("user_libraries")
            .delete()
            .eq("library_name", i)
            .eq("email", email)
            .execute()
        )

    async def delete(self, db: Client, *, i: str) -> Library | None:
        db.table("user_libraries").delete().eq("library_name", i).execute()
        return await super().delete(db, i=i)


library_crud = CRUDLibrary(Library)
