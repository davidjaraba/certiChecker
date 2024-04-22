from pydantic import BaseModel, ConfigDict

from typing import Optional


class CreateURLDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str

    company_id: int


class ResponseURLDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str

    company_id: int

    company_name: str

    created_at: str


class UpdateURLDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_id: Optional[int] = None
