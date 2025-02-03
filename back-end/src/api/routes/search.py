import re
import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from nlb_catalogue_client.models.bad_request_error import BadRequestError
from nlb_catalogue_client.types import UNSET

# from nlb_catalogue_client.api.catalogue import get_search_titles
# from nlb_catalogue_client.models.search_titles_response_v2 import SearchTitlesResponseV2
from nlb_catalogue_client.api.catalogue import get_get_titles
from nlb_catalogue_client.models.get_titles_response_v2 import GetTitlesResponseV2


from src.api.deps import SDBDep, CurrentUser, NLBClientDep
from src.crud.user_search import user_search_crud
from src.modals.book_info import BookInfo
from src.modals.book_search import SearchResponse
from src.modals.user_search import UserSearchCreate


router = APIRouter()


@router.get("")
async def search_books(
    db: SDBDep,
    nlb: NLBClientDep,
    user: CurrentUser,
    keyword: str = "",
    offset: Optional[int] = 0,
    limit: Optional[int] = 25,
) -> SearchResponse:
    """Calls NLB API GetTitles Search and show results
    in search_table.html
    """
    if not user or not user.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is not found for user")

    if not keyword:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Keyword is empty in params")

    # Get titles from NLB API
    # response = await get_search_titles.asyncio_detailed(
    #     client=nlb,
    #     keywords=keyword,
    #     offset=offset if offset else UNSET,
    #     limit=limit if limit else UNSET,
    # )
    response = await get_get_titles.asyncio_detailed(
        client=nlb,
        # Remove non-alphanumeric and spaces char
        keywords=re.sub(r"[^A-Za-z0-9 ]+", "", keyword),
        offset=offset if offset else UNSET,
        limit=limit if limit else UNSET,
    )

    # Raise error if NLB API throw error
    # if not isinstance(response.parsed, SearchTitlesResponseV2):
    if not isinstance(response.parsed, GetTitlesResponseV2):
        # HACK: Since NLB api implement 404 as BadRequestError,
        # work around is to catch it earlier
        if isinstance(response.parsed, BadRequestError):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "No search results are found"
            )
        if response.status_code == 429:
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS, "Rate limited by NLB API"
            )

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(response.parsed))

    # Return 404 if no response is found
    if response.parsed.total_records == 0 or not response.parsed.titles:
        # Return empty table
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No search results are found")

    # Track user search in db
    await user_search_crud.create(
        db,
        obj_in=UserSearchCreate(
            email=user.email,
            search_time=int(
                time.mktime(datetime.now().timetuple()),
            ),
            Title=keyword,
            Author="",
        ),
    )

    total_records = (
        response.parsed.total_records if response.parsed.total_records else 0
    )
    has_more_records = (
        response.parsed.has_more_records if response.parsed.has_more_records else False
    )

    return SearchResponse(
        total_records=total_records,
        has_more_records=has_more_records,
        titles=[
            BookInfo.from_title(title)
            for title in response.parsed.titles
            if title.format_.name == "Book"
        ],
    )
