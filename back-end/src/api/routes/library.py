from fastapi import APIRouter, status, HTTPException

from src.api.deps import SDBDep, CurrentUser
from src.crud.library import library_crud
from src.modals.library import Library
from src.modals.library_response import LibraryResponse

router = APIRouter()


@router.get("")
async def get_libraries(
    user: CurrentUser,
    db: SDBDep,
) -> list[LibraryResponse]:
    """Get all libraries in the database and whether is library favourite"""
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        libraries = await library_crud.get_all(db)
        libraries_fav = await library_crud.get_multi_by_owner(db, email=user.email)
        favourite = {lib.name for lib in libraries_fav} if libraries_fav else {}
        return [
            LibraryResponse(**lib.model_dump(), isFavourite=lib.name in favourite)
            for lib in libraries
        ]

    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e


@router.get("/{name}")
async def get_library(
    name: str,
    user: CurrentUser,
    db: SDBDep,
) -> Library:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        library = await library_crud.get(db, i=name)
        if not library:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Library of {name} could not be found from database.",
            )

        return library

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e


@router.post("/{name}", status_code=status.HTTP_201_CREATED)
async def favourite_library(
    name: str,
    db: SDBDep,
    user: CurrentUser,
) -> None:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        await library_crud.create_owner(
            db,
            name=name,
            email=user.email,
        )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e


@router.delete("/{name}")
async def unfavourite_library(name: str, db: SDBDep, user: CurrentUser):
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        await library_crud.delete_owner(db, i=name, email=user.email)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e
