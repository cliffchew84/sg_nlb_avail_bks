from asyncio import sleep
from fastapi import APIRouter, status, HTTPException
from google.cloud import tasks_v2
from nlb_catalogue_client.api.catalogue import (
    get_get_availability_info,
    get_get_title_details,
)
from nlb_catalogue_client.models.get_availability_info_response_v2 import (
    GetAvailabilityInfoResponseV2,
)
from nlb_catalogue_client.models.get_title_details_response_v2 import (
    GetTitleDetailsResponseV2,
)

from src.api.deps import SDBDep, CurrentUser, NLBClientDep
from src.crud.book_avail import book_avail_crud
from src.crud.book_info import book_info_crud
from src.crud.book_outdated_bid import book_outdated_bid_crud
from src.modals.book_avail import BookAvail, BookAvailCreate
from src.modals.book_info import BookInfoCreate
from src.modals.book_response import BookResponse
from src.utils import create_http_task

router = APIRouter()


@router.get("")
async def get_books(
    user: CurrentUser,
    db: SDBDep,
) -> list[BookResponse]:
    """Get all books that user marked as favourite"""
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    try:
        book_infos = await book_info_crud.get_multi_by_owner(db, email=user.email)
        return [
            BookResponse(
                **book_info.model_dump(),
                avails=await book_avail_crud.get_multi_by_owner(
                    db, email=user.email, BIDs=[book_info.BID]
                ),
            )
            for book_info in book_infos
        ]

    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e


@router.get("/{bid}")
async def get_book(
    bid: int, user: CurrentUser, db: SDBDep, nlb: NLBClientDep, live: bool = False
) -> BookResponse:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    book_saved = True  # Book was saved before in database
    try:
        book_info = await book_info_crud.get(db, i=str(bid))
        if not book_info:
            book_saved = False
            # Book infomation does not exist in database,
            # querying from NLB API instead
            response_info = await get_get_title_details.asyncio_detailed(
                client=nlb, brn=bid
            )
            if not isinstance(response_info.parsed, GetTitleDetailsResponseV2):
                if response_info.status_code == 404:
                    raise HTTPException(
                        status.HTTP_404_NOT_FOUND, str(response_info.parsed)
                    )
                if response_info.status_code == 429:
                    raise HTTPException(
                        status.HTTP_429_TOO_MANY_REQUESTS, "Rate limited by NLB API"
                    )

                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR, str(response_info.parsed)
                )

            book_info = BookInfoCreate.from_nlb(response_info.parsed)

        if book_saved and not live:
            # If book was saved, its availiblity exists in database
            # If fetch_live param is set, live data will be queries regardless
            book_avail = await book_avail_crud.get_multi_by_owner(
                db, email=user.email, BIDs=[bid]
            )
        else:
            print("Querying live:")
            # Book availablitiy does not exist in database,
            # querying from NLB API instead
            response_avail = await get_get_availability_info.asyncio_detailed(
                client=nlb, brn=bid
            )
            if (
                not isinstance(
                    response_avail.parsed, GetAvailabilityInfoResponseV2
                )  # ErrorResponse
            ):
                if response_avail.status_code == 429:
                    raise HTTPException(
                        status.HTTP_429_TOO_MANY_REQUESTS, "Rate limited by NLB API"
                    )
                if response_avail.status_code == 404:
                    # Book availibity does not exist, continues as book_avail is None
                    pass

                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR, str(response_avail.parsed)
                )

            book_avail = [
                BookAvailCreate.from_nlb(item)
                for item in response_avail.parsed.items or []
            ]

            # Save book avail to db if book was saved before
            if book_saved:
                await book_avail_crud.upsert(db, obj_ins=book_avail)

        return BookResponse(**book_info.model_dump(), avails=book_avail)

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        print(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e


@router.post("/{bid}", status_code=status.HTTP_201_CREATED)
async def like_book(
    bid: int,
    db: SDBDep,
    nlb: NLBClientDep,
    user: CurrentUser,
) -> BookResponse:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    # Makes API to bk info and bk avail
    response_info = await get_get_title_details.asyncio_detailed(client=nlb, brn=bid)
    if not isinstance(response_info.parsed, GetTitleDetailsResponseV2):
        if response_info.status_code == 404:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(response_info.parsed))
        if response_info.status_code == 429:
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS, "Rate limited by NLB API"
            )

        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, str(response_info.parsed)
        )

    response_avail = await get_get_availability_info.asyncio_detailed(
        client=nlb, brn=bid
    )
    if (
        not isinstance(
            response_avail.parsed, GetAvailabilityInfoResponseV2
        )  # ErrorResponse
        or response_avail.parsed.total_records == 0
    ):
        if response_avail.status_code == 429:
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS, "Rate limited by NLB API"
            )

        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, str(response_avail.parsed)
        )

    # Do all the adding at the end, after everything is confirmed
    # Insert and Update if conflict on book availability
    try:
        book_info_result = BookInfoCreate.from_nlb(response_info.parsed)
        await book_info_crud.create_book_by_user(
            db,
            obj_in=book_info_result,
            email=user.email,
        )
        all_avail_bks = [
            BookAvailCreate.from_nlb(item) for item in response_avail.parsed.items or []
        ]
        await book_avail_crud.upsert(
            db,
            obj_ins=all_avail_bks,
        )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e

    return BookResponse(**book_info_result.model_dump(), avails=all_avail_bks)


async def update_book_avail(db, nlb, bid_no: int) -> list[BookAvail]:
    """
    - Takes in single BID to get avail info
    - Processes data for Supabase
    - Delete existing Supabase data if necessary
    - Inject new data into Supabase
    """

    # Make API call on book availability
    response = await get_get_availability_info.asyncio_detailed(client=nlb, brn=bid_no)
    if (
        not isinstance(response.parsed, GetAvailabilityInfoResponseV2)  # ErrorResponse
        or response.parsed.total_records == 0
    ):
        if response.status_code == 200:
            # If Book avail have no records
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(response.parsed))

        if response.status_code == 429:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, str(response.parsed))

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(response.parsed))

    # Insert and Update if conflict on book availability
    try:
        all_avail_bks = [
            BookAvailCreate.from_nlb(item) for item in response.parsed.items or []
        ]
        book_avails = await book_avail_crud.upsert(
            db,
            obj_ins=all_avail_bks,
        )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error occured with database transaction.",
        ) from e
    return book_avails


@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update_books(
    db: SDBDep,
    nlb: NLBClientDep,
    user: CurrentUser,
    query_per_min: int = 15,
    recurse: bool = False,
):
    """Updates availability of all saved books"""
    if user is not None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Only service account can trigger this endpoint",
        )

    outdated_books = await book_outdated_bid_crud.get_all(db)
    if outdated_books and recurse:
        # Schedule task for recursive update every 1 minute
        create_http_task(
            tasks_v2.HttpMethod.PUT,
            path="/books",
            body={},
            query=dict(query_per_min=query_per_min, recurse=recurse),
            scheduled_seconds_from_now=40,
        )
        print("Created new google cloud task")

    fail_bid = []
    # TODO: Do limiting on database side instead
    for book in outdated_books[:query_per_min]:
        try:
            await update_book_avail(db, nlb, book.BID)
            print(f"Updated book BID: {book.BID}")
            await sleep(1)  # To comply 1 request per second rate-limit
        except Exception as e:
            if isinstance(e, HTTPException):
                if e.status_code == 404:
                    # delete book avail from DB if no records was found on book
                    await book_avail_crud.delete_by_bid(db, bid=book.BID)

            print(f"Update fail for BID:{book.BID}: Error {e}")
            fail_bid.append(book.BID)


@router.put("/{bid}")
async def update_book(
    bid: int, db: SDBDep, nlb: NLBClientDep, user: CurrentUser
) -> list[BookAvail]:
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    book_avail = await update_book_avail(db, nlb, bid)
    return book_avail


@router.delete("/{bid}")
async def unlike_book(bid: int, db: SDBDep, user: CurrentUser):
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    bid_no = str(bid)

    await book_info_crud.delete_owner(db, i=bid_no, email=user.email)
    return
