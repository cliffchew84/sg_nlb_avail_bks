from fastapi import APIRouter, HTTPException, status

from src.api.deps import SDBDep, CurrentUser
from src.crud.users import user_crud
from src.modals.users import User, UserUpdate

router = APIRouter()


@router.get("")
async def read_user(db: SDBDep, user: CurrentUser) -> User:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    user_model = await user_crud.get(db, i=user.email)
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user_model


@router.put("")
async def update_user(
    db: SDBDep,
    user: CurrentUser,
    user_update: UserUpdate,
) -> User:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    # Do not allow to update email
    if user_update.email != user.email:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Email cannot be updated in this endpoint"
        )

    try:
        updated_user = await user_crud.update(db, i=user.email, obj_in=user_update)
        return updated_user
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: SDBDep, user: CurrentUser, client: SDBDep):
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        # Delete user from supabase auth and remove user table
        client.auth.admin.delete_user(user.id)
        deleted_user = await user_crud.delete(db, i=user.email)
        if not deleted_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e
