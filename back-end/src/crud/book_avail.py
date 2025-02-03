from typing import Optional

from supabase import Client

from src.crud.base import CRUDBase
from src.crud.book_info import book_info_crud
from src.modals.book_avail import (
    BookAvail,
    BookAvailCreate,
    BookAvailUpdate,
)


class CRUDBookAvail(CRUDBase[BookAvail, BookAvailCreate, BookAvailUpdate]):
    async def create(
        self,
        db: Client,
        *,
        obj_in: BookAvailCreate,
        excludes: Optional[set[str]] = {"UpdateTime"},
    ) -> BookAvail:
        return await super().create(db, obj_in=obj_in, excludes=excludes)

    async def get(self, db: Client, *, i: str) -> BookAvail | None:
        return await super().get(db, i=i)

    async def get_all(self, db: Client) -> list[BookAvail]:
        return await super().get_all(db)

    async def get_all_by_bid(self, db: Client, bid: int) -> list[BookAvail]:
        response = db.table(self.model.table_name).select("*").eq("BID", bid).execute()
        return [self.model(**item) for item in response.data]

    async def get_multi_by_owner(
        self, db: Client, *, email: str, BIDs: Optional[list[int]] = None
    ) -> list[BookAvail]:
        if BIDs is None:
            book_infos = await book_info_crud.get_multi_by_owner(db, email=email)
            BIDs = [book_info.BID for book_info in book_infos]
        response = (
            db.table(self.model.table_name).select("*").in_("BID", BIDs).execute()
        )
        return [BookAvail(**item) for item in response.data]

    async def update(
        self,
        db: Client,
        *,
        obj_in: BookAvailUpdate,
        i: str,
        excludes: Optional[set[str]] = {"UpdateTime"},
    ) -> BookAvail:
        return await super().update(db, obj_in=obj_in, i=i, excludes=excludes)

    async def upsert(
        self,
        db: Client,
        *,
        obj_ins: list[BookAvailCreate],
        excludes: Optional[set[str]] = {"UpdateTime"},
        delete_excluded: bool = True,
    ) -> list[BookAvail]:
        updated_book_avail = await super().upsert(
            db, obj_ins=obj_ins, excludes=excludes
        )
        updated_book_avail_itemNo = {updated.ItemNo for updated in updated_book_avail}
        if updated_book_avail and delete_excluded:
            old_book_avail = await self.get_all_by_bid(
                db, bid=updated_book_avail[0].BID
            )
            old_book_avail_itemNo = {book.ItemNo for book in old_book_avail}
            for remove_ItemNo in old_book_avail_itemNo.difference(
                updated_book_avail_itemNo
            ):
                await self.delete(db, i=remove_ItemNo)

        return updated_book_avail

    async def delete(self, db: Client, *, i: str) -> BookAvail | None:
        return await super().delete(db, i=i)

    async def delete_by_bid(self, db: Client, *, bid: int) -> BookAvail | None:
        response = db.table(self.model.table_name).delete().eq("BID", bid).execute()
        deleted = response.data
        if not deleted:
            return None
        return self.model(**deleted[0])


book_avail_crud = CRUDBookAvail(BookAvail)
