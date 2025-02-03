from fastapi import APIRouter, status, HTTPException

from src.api.deps import SDBDep, CurrentUser
from src.crud.notifications import notification_crud
from src.modals.notifications import Notification, NotificationUpdate

router = APIRouter()


@router.get("")
async def get_notifications(
    user: CurrentUser,
    db: SDBDep,
) -> list[Notification]:
    """Get all libraries in the database and whether is library favourite"""
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        return await notification_crud.get_multi_by_owner(db, email=user.email)

    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e


@router.post("/{nid}/read")
async def read_notification(
    nid: str,
    db: SDBDep,
    user: CurrentUser,
) -> None:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        notification = await notification_crud.get(db, i=nid)
        if not notification:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Notification of {nid} could not be found from database.",
            )
        if notification.email != user.email:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "User is not authorized to read this notification.",
            )

        await notification_crud.update(
            db,
            obj_in=NotificationUpdate(isRead=True),
            i=nid,
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e


# Unread notifications
@router.post("/{nid}/unread")
async def unread_notification(
    nid: str,
    db: SDBDep,
    user: CurrentUser,
) -> None:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        notification = await notification_crud.get(db, i=nid)
        if not notification:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Notification of {nid} could not be found from database.",
            )
        if notification.email != user.email:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "User is not authorized to read this notification.",
            )

        await notification_crud.update(
            db,
            obj_in=NotificationUpdate(**notification.model_dump(), isRead=False),
            i=nid,
        )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e
