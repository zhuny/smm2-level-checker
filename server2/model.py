import datetime
from typing import List, Optional, Set

from pydantic import BaseModel, Field


class Team(BaseModel):
    id: str  # url_slug
    team_name: str
    discord_invite: str
    twitter_user: str
    primary_color: str
    secondary_color: str
    max_difficulty: int


class Difficulty(BaseModel):
    team_slug: str
    difficulty: int
    clears: int
    likes: int

    created_at: datetime.datetime


class Level(BaseModel):
    id: str  # code
    code: str
    creator: str
    maker_id: Optional[str]
    level_name: str
    tags: Set[str] = Field(default_factory=set)
    difficulty_list: List[Difficulty] = Field(default_factory=list)


class LevelClear(BaseModel):
    level_code: str
    user_id: str
    clear_at: datetime.datetime
