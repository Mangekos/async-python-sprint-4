from fastapi import APIRouter, Request
from fastapi.responses import Response
from api.schema import Link

from models.links import Links
from db.db import (
    add_crossings,
    add_link,
    del_link,
    find_full_link,
    find_short_link,
    get_all_links,
)

router_links = APIRouter()


@router_links.get("/", status_code=200)
async def get_links(request: Request) -> Response:
    """
    Returns all links
    """
    links: list[Links] = await get_all_links()
    links_json = {
        "links": [
            {
                "short_link": link.id,
                "full_link": link.full_link,
                "creator": link.creator,
            }
            for link in links
        ]
    }
    return links_json


@router_links.post("/add", status_code=201)
async def add_short_link(request: Request, link: Link) -> int:
    """
    Returns the id of the record with the passed link
    """
    short_link: Links = await find_short_link(link.full_link)
    if short_link is None and request.client:
        short_link: Links = await add_link(link.full_link, request.client.host)
    short_link: Links = await add_link(link.full_link, link.creator)
    return short_link.id


@router_links.get("/del/{short_link}")
async def del_short_link(short_link: int) -> Response:
    """
    Removes the link
    """
    if await del_link(int(short_link)):
        return Response(status_code=204)
    return Response(status_code=404)


@router_links.get("/get/{short_link}")
async def get_full_link(short_link, request: Request) -> Response:
    """
    Returns the full link
    """
    full_link: Links = await find_full_link(int(short_link))
    if full_link is None:
        return Response(status_code=404)
    if full_link.remove:
        return Response(status_code=410)
    if request.client:
        await add_crossings(full_link, request.client.host)
    return Response(content=full_link.full_link, status_code=200)
