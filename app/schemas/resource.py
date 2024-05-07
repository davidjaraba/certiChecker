from pydantic import BaseModel, ConfigDict
from enum import Enum

from typing import Optional


class ResourceType(Enum):
    HTML = 'HTML'
    IMG = 'IMG'
    DOC = 'DOC'


class CreateResourceDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: ResourceType

    url_id: str

    path_file: str


class ResponseResourceDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str

    type: ResourceType

    url_id: str

    path_file: str

    created_at: str


class UpdateResourceDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: Optional[ResourceType] = None

    url_id: Optional[str] = None

    path_file: Optional[str] = None