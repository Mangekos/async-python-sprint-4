from pydantic import BaseModel


class Link(BaseModel):
    full_link: str
    creator: str
