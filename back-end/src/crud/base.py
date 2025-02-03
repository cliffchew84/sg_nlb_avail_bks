from typing import Generic, Optional, TypeVar

from supabase import Client

from src.modals.base import CreateBase, ResponseBase, UpdateBase

ModelT = TypeVar("ModelT", bound=ResponseBase)
CreateSchemaT = TypeVar("CreateSchemaT", bound=CreateBase)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=UpdateBase)


class CRUDBase(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    """Basic CRUD operations"""

    def __init__(self, model: type[ModelT]):
        self.model = model

    async def get(self, db: Client, *, i: str) -> ModelT | None:
        """get by table_name by id"""
        response = (
            db.table(self.model.table_name).select("*").eq(self.model.pk, i).execute()
        )
        got = response.data
        return self.model(**got[0]) if got else None

    async def get_all(self, db: Client) -> list[ModelT]:
        """get all by table_name"""
        response = db.table(self.model.table_name).select("*").execute()
        return [self.model(**item) for item in response.data]

    async def get_multi_by_owner(self, db: Client, *, email: str) -> list[ModelT]:
        """get by owner,use it  if rls failed to use"""
        response = (
            db.table(self.model.table_name).select("*").eq("email", email).execute()
        )
        return [self.model(**item) for item in response.data]

    async def create(
        self, db: Client, *, obj_in: CreateSchemaT, excludes: Optional[set[str]] = None
    ) -> ModelT:
        """create by CreateSchemaT"""
        response = (
            db.table(self.model.table_name)
            .insert(obj_in.model_dump(exclude=excludes))
            .execute()
        )

        return self.model(**response.data[0])

    async def update(
        self,
        db: Client,
        *,
        obj_in: UpdateSchemaT,
        i: str,
        excludes: Optional[set[str]] = None,
    ) -> ModelT:
        """update by UpdateSchemaT"""
        response = (
            db.table(self.model.table_name)
            .update(obj_in.model_dump(exclude=excludes, exclude_unset=True))
            .eq(self.model.pk, i)
            .execute()
        )
        updated = response.data
        return self.model(**updated[0])

    async def upsert(
        self,
        db: Client,
        *,
        obj_ins: list[CreateSchemaT],
        excludes: Optional[set[str]] = None,
    ) -> list[ModelT]:
        """upsert by UpdateSchemaT"""
        response = (
            db.table(self.model.table_name)
            .upsert([obj_in.model_dump(exclude=excludes) for obj_in in obj_ins])
            .execute()
        )
        updateds = response.data
        return [self.model(**updated) for updated in updateds]

    async def delete(self, db: Client, *, i: str) -> ModelT | None:
        """remove by UpdateSchemaT"""
        response = (
            db.table(self.model.table_name).delete().eq(self.model.pk, i).execute()
        )
        deleted = response.data
        if not deleted:
            return None
        return self.model(**deleted[0])
