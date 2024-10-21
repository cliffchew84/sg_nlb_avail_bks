import time
from typing import Optional

from fastapi import (
    FastAPI,
    status,
    Request,
    Form,
    Depends,
    Cookie,
)
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from src import m_db
from src import supa_db as s_db
from src import nlb_api as n_api
from src import process as p
from src.api import api
from src.api.deps import UsernameDep
from src.config import settings
from src.utils import templates


# Think about adding back mongoDB stuff
# user_status

# Environment setup
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Application code
app = FastAPI(
    title=settings.APP_NAME, version=settings.VERSION, description=settings.DESCRIPTION
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    return s_db.connect_sdb()


def username_email_resol(user_info: str):
    """In the current new flow, username == email
    To cover legacy situation where username != email
    """
    email, username = user_info.split(" | ")
    if not username:
        username = email
    return username


@app.get("/main", response_class=HTMLResponse)
async def main(request: Request, user_info: str = Cookie(None), db=Depends(get_db)):
    if user_info:
        username = username_email_resol(user_info)

        # Continue to extract user book info
        query = s_db.q_user_bks(username)
        response = p.process_user_bks(query)

        # Processing necessary statistics
        all_unique_books = p.get_unique_bks(response)
        all_avail_books = p.get_avail_bks(response)
        unique_libs = p.get_unique_libs(response)
        avail_bks_by_lib = p.get_avail_bks_by_lib(response)
        lib_book_summary = p.get_lib_bk_summary(unique_libs, avail_bks_by_lib)

        mdb = m_db.connect_mdb()
        mdb = mdb["nlb"]
        update_status = None
        if m_db.q_status(db=mdb, username=username):
            update_status = " "

        # Check if user has a default library
        user_info = s_db.q_user_info(db, username)
        preferred_lib = user_info.get("preferred_lib")

        if preferred_lib:
            preferred_lib = preferred_lib.lower()
            output = []
            for book in response:
                if preferred_lib in book["BranchName"].lower():
                    output.append(book)
        else:
            preferred_lib = "all"
            output = response

        lib_avail = len(p.get_avail_bks(output))
        lib_all = len(p.get_unique_bks(output))

        return templates.TemplateResponse(
            "main.html",
            {
                "request": request,
                "username": username,
                "api_data": output,
                "all_avail_books": all_avail_books,
                "all_unique_books": all_unique_books,
                "avail_books": avail_bks_by_lib,
                "lib_book_summary": lib_book_summary,
                "lib_avail": lib_avail,
                "lib_all": lib_all,
                "library": preferred_lib,
                "status": update_status,
            },
        )

    else:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


# Start my edits from here
@app.get("/lib/{library}/", response_class=HTMLResponse)
async def show_avail_bks(
    request: Request,
    library: Optional[str],
    db=Depends(get_db),
    user_info: str = Cookie(None),
):
    if user_info:
        username = username_email_resol(user_info)
        mdb = m_db.connect_mdb()
        mdb = mdb["nlb"]
        update_status = None
        if m_db.q_status(db=mdb, username=username):
            update_status = " "

        # Query entire user books - Inefficient
        query = s_db.q_user_bks(username=username)
        response = p.process_user_bks(query)
        all_unique_books = p.get_unique_bks(response)
        all_avail_books = p.get_avail_bks(response)

        if library != "all":
            output = []
            for book in response:
                if library in book["BranchName"].lower():
                    output.append(book)
        else:
            output = response

        lib_avail = len(p.get_avail_bks(output))
        lib_all = len(p.get_unique_bks(output))

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "username": username,
                "api_data": output,
                "library": library,
                "all_avail_books": all_avail_books,
                "all_unique_books": all_unique_books,
                "lib_avail": lib_avail,
                "lib_all": lib_all,
                "status": update_status,
            },
        )

    else:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@app.get("/book_status/{book_saved}")
async def book_status_progress_bar(
    request: Request, book_saved: int, db=Depends(get_db), user_info: str = Cookie(None)
):
    try:
        username = username_email_resol(user_info)
        mdb = m_db.connect_mdb()
        mdb = mdb["nlb"]
        user_info = m_db.q_user_info(db=mdb, username=username)
        books_updated = user_info.get("books_updated")
        title = user_info.get("title")

        print(books_updated)
        print(title)

        progress = 0
        if books_updated > 0:
            progress = (books_updated / book_saved) * 100

        update_status = None
        if m_db.q_status(db=mdb, username=username):
            update_status = " "

        return templates.TemplateResponse(
            "/partials/update_status_text.html",
            {
                "request": request,
                "progress": progress,
                "TitleName": title,
                "total_books": book_saved,
                "book_count": books_updated,
                "status": update_status,
            },
        )
    except:
        return templates.TemplateResponse(
            "/partials/update_status_text.html",
            {
                "request": request,
            },
        )


@app.post("/complete-update/", response_class=HTMLResponse)
async def update_book(request: Request):
    return templates.TemplateResponse("complete-status.html", {"request": request})


@app.get("/update_header", response_class=HTMLResponse)
async def update_header(
    request: Request, db=Depends(get_db), user_info: str = Cookie(None)
):
    username = username_email_resol(user_info)
    query = s_db.q_user_bks(username=username)
    response = p.process_user_bks(query)

    # Processing necessary statistics
    all_unique_books = p.get_unique_bks(response)
    all_avail_books = p.get_avail_bks(response)
    unique_libs = p.get_unique_libs(response)
    avail_bks_by_lib = p.get_avail_bks_by_lib(response)
    lib_book_summary = p.get_lib_bk_summary(unique_libs, avail_bks_by_lib)

    mdb = m_db.connect_mdb()
    mdb = mdb["nlb"]
    update_status = None
    if m_db.q_status(db=mdb, username=username):
        update_status = " "

    # Check if user has a default library
    user_info = s_db.q_user_info(db, username)
    preferred_lib = user_info.get("preferred_lib")

    if preferred_lib:
        preferred_lib = preferred_lib.lower()
        output = []
        for book in response:
            if preferred_lib in book["BranchName"].lower():
                output.append(book)

    else:
        preferred_lib = "all"
        output = response

    lib_avail = len(p.get_avail_bks(output))
    lib_all = len(p.get_unique_bks(output))

    return templates.TemplateResponse(
        "navbar.html",
        {
            "request": request,
            "username": username,
            "api_data": output,
            "all_avail_books": all_avail_books,
            "all_unique_books": all_unique_books,
            "avail_books": avail_bks_by_lib,
            "lib_book_summary": lib_book_summary,
            "lib_avail": lib_avail,
            "lib_all": lib_all,
            "library": preferred_lib,
            "status": update_status,
        },
    )


@app.post("/ingest_books_navbar", response_class=HTMLResponse)
async def ingest_books_navbar(
    request: Request,
    bids: list = Form(...),
    db=Depends(get_db),
    user_info: str = Cookie(None),
):
    username = username_email_resol(user_info)
    for bid in bids:
        print(bid)
        # Makes API to bk info and bk avail and ingest the data into DB
        bk_title = n_api.get_process_bk_info(bid_no=bid)

        time.sleep(2)
        update_bk_avail_supa(db, bid)

        # Do all the adding at the end, after everything is confirmed
        # This also doesn't require any time.sleep() as this is with my own DB
        s_db.add_user_book(db=db, username=username, bid_no=bid)
        s_db.add_book_info(db=db, books_info=bk_title)

        print("print started book_available update")

    # Update the books calculation on the navbar
    query = s_db.q_user_bks(username=username)
    response = p.process_user_bks(query)

    # Processing necessary statistics
    all_unique_books = p.get_unique_bks(response)
    all_avail_books = p.get_avail_bks(response)
    unique_libs = p.get_unique_libs(response)
    avail_bks_by_lib = p.get_avail_bks_by_lib(response)
    lib_book_summary = p.get_lib_bk_summary(unique_libs, avail_bks_by_lib)

    return templates.TemplateResponse(
        "navbar.html",
        {
            "request": request,
            "username": username,
            "all_avail_books": all_avail_books,
            "all_unique_books": all_unique_books,
            "lib_book_summary": lib_book_summary,
        },
    )


# Main Page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request, username: UsernameDep):
    if username:
        # Redirect to main if user is logged in
        return RedirectResponse("/main")
    return templates.TemplateResponse("google_page.html", {"request": request})


# Logout route to remove the JWT token
@app.get("/logout")
def logout():
    response = RedirectResponse("/")
    response.delete_cookie("user_info")
    return response
