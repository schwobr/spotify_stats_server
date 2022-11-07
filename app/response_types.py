from enum import StrEnum, auto
from typing import Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class Type(StrEnum):
    album = auto()
    artist = auto()
    track = auto()
    playlist = auto()
    episode = auto()
    ad = auto()
    show = auto()
    unknown = auto()


class DeviceType(StrEnum):
    computer = auto()
    smartphone = auto()
    spearker = auto()


class RepeatState(StrEnum):
    off = auto()
    track = auto()
    context = auto()


class ShuffleState(StrEnum):
    on = auto()
    off = auto()


class PlaybackAction(StrEnum):
    interrupting_playback = auto()
    pausing = auto()
    resuming = auto()
    seeking = auto()
    skipping_next = auto()
    skipping_prev = auto()
    toggling_repeat_context = auto()
    toggling_shuffle = auto()
    toggling_repeat_track = auto()
    transferring_playback = auto()


class Image(BaseModel):
    url: str
    height: int
    width: int


class Item(BaseModel):
    id: str
    name: str
    href: str
    uri: str
    type: Type
    external_urls: Optional[Dict[str, str]] = None
    external_ids: Optional[Dict[str, str]] = None
    available_markets: Optional[List[str]] = None
    images: Optional[List[Image]] = None
    popularity: Optional[int] = None
    restrictions: Optional[Dict[str, str]] = None


ItemT = TypeVar("ItemT", Item)


class ItemList(GenericModel, Generic[ItemT]):
    href: str
    items: List[ItemT]
    limit: int
    offset: int
    total: int
    next: Optional[str] = None
    previous: Optional[str] = None


class Followers(BaseModel):
    total: int
    href: Optional[str] = None


class Artist(Item):
    followers: Optional[Followers] = None
    genres: Optional[List[str]] = None


class Album(Item):
    album_type: str
    total_tracks: int
    release_date: str
    release_date_precision: str
    artists: List[Artist]
    tracks: ItemList["Track"]
    album_group: Optional[str] = None


class Track(Item):
    album: Album
    artists: List[Artist]
    disc_number: int
    duration_ms: int
    explicit: bool
    track_number: int
    is_local: bool
    preview_url: Optional[str] = None
    is_playable: Optional[bool] = None
    linked_from: Optional["Track"] = None


class Device(BaseModel):
    id: str
    name: str
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    type: DeviceType
    volume_percent: int


class Context(BaseModel):
    type: Type
    href: str
    uri: str
    externel_urls: Optional[Dict[str, str]] = None


class PlaybackState(BaseModel):
    device: Device
    repeat_state: RepeatState
    shuffle_state: ShuffleState
    timestamp: int
    progress_ms: int
    is_playing: bool
    item: Track
    currently_playing_type: Type
    actions: Dict[PlaybackAction, bool]
    progress_ms: Optional[int] = None
    context: Optional[Context] = None
