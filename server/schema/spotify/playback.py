from pydantic import BaseModel,Field
from typing import List, Optional,Literal,Union,Annotated
from .top_items import ExternalUrls,TrackObjects

class Cursors (BaseModel):
    after: Optional[str] = None
    before: Optional[str] = None

class Context (BaseModel):
    type: str 
    href: str 
    external_urls: ExternalUrls
    uri: str

class RecentlyPlayedItem (BaseModel):
    track: TrackObjects
    played_at: str
    context: Optional[Context] = None


class RecentlyPlayed (BaseModel):
    """
    Docstring for RecentlyPlayed
    href: str -> A link to the Web API endpoint returning the full result of the request items: [ { track: track object, played_at: datetime, context: context object } ] -> An array of objects containing a track and the date and time it was played limit: int -> The maximum number of items in the response (as set in the query or by default) next: str -> URL to the next page of items. (null if none) cursors: { after: str } -> A cursor object containing a cursor before and after the current set of items. Can be used to fetch the next or previous page of items. (Deprecated in favor of next and previous URLs) total: int -> The total number of items available to return. Can be used with the limit and offset query parameters to paginate through all available items. 
    limit: int -> The maximum number of items in the response (as set in the query or by default) 
    next: Optional[str] -> URL to the next page of items.(null if none)
    cursors: {after -> Optional[str]} -> A cursor object containing a cursor before and after the current set of items. Can be used to fetch the next or previous page of items , before: Optional[str] = None -> The cursor to use as key to find the previous pages of items.
    items: List[RecentlyPlayedItem] -> An array of objects containing a track and the date and time it was played.
    """
    href: str
    limit: int
    next: Optional[str] = None
    cursors: Optional[Cursors] = None
    items: List[RecentlyPlayedItem]
