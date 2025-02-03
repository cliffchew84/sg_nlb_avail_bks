from typing import Optional

from supabase import Client

from src.crud.base import CRUDBase
from src.modals.users import User
from src.modals.book_info import (
    BookInfo,
    BookInfoCreate,
    BookInfoUpdate,
)
from src.modals.user_books import UserBook, UserBookCreate


class CRUDBookInfo(CRUDBase[BookInfo, BookInfoCreate, BookInfoUpdate]):
    async def create(
        self,
        db: Client,
        *,
        obj_in: BookInfoCreate,
        excludes: Optional[set[str]] = None,
    ) -> BookInfo:
        return await super().create(db, obj_in=obj_in, excludes=excludes)

    async def create_book_by_user(
        self,
        db: Client,
        obj_in: BookInfoCreate,
        email: str,
        excludes: Optional[set[str]] = None,
    ) -> BookInfo:
        result = await super().upsert(db, obj_ins=[obj_in], excludes=excludes)

        # Add user book relationship table
        user_book = UserBookCreate(email=email, BID=obj_in.BID)
        db.table(UserBook.table_name).insert(user_book.model_dump()).execute()

        return result[0]

    async def get(self, db: Client, *, i: str) -> BookInfo | None:
        return await super().get(db, i=i)

    async def get_all(self, db: Client) -> list[BookInfo]:
        return await super().get_all(db)

    async def get_multi_by_owner(self, db: Client, *, email: str) -> list[BookInfo]:
        response = (
            db.table("user_books")
            .select(f"*, {self.model.table_name}(*)")
            .eq("email", email)
            .execute()
        )
        return [
            BookInfo(**item[self.model.table_name])
            for item in response.data
            if self.model.table_name in item
        ]

    async def get_owners(self, db: Client, *, i: str) -> list[User]:
        """Get users that owns the given bid"""
        response = (
            db.table("user_books")
            .select(f"*, {User.table_name}(*)")
            .eq("BID", i)
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
        obj_in: BookInfoUpdate,
        i: str,
        excludes: Optional[set[str]] = None,
    ) -> BookInfo:
        return await super().update(db, obj_in=obj_in, i=i, excludes=excludes)

    async def delete_owner(self, db: Client, *, i: str, email: str):
        (db.table("user_books").delete().eq("BID", i).eq("email", email).execute())

    async def delete(self, db: Client, *, i: str) -> BookInfo | None:
        db.table("user_books").delete().eq("BID", i).execute()
        return await super().delete(db, i=i)


book_info_crud = CRUDBookInfo(BookInfo)
