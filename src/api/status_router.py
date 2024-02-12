from fastapi import APIRouter
from fastapi.responses import Response

from db.db import get_crossings, ping

router_status = APIRouter()


async def paginator_response() -> dict[str, int]:
    return {"offset": 0, "max-result": 3, "full-info": False}


@router_status.get("/ping")
async def ping_db() -> Response:
    """
    Ping the database
    """
    if await ping():
        return Response(status_code=200)
    else:
        return Response(status_code=500)


@router_status.post("/status/{link}")
async def get_status(
    link: int, full: bool = False, offset: int = 0, max: int = 10
) -> int | str:
    """
    Returns the status of the link
    """
    crossings: str = await get_crossings(link)
    if not full:
        return len(crossings)
    new_cross: str = crossings[offset: offset + max]
    return new_cross
