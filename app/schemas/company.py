from pydantic import BaseModel, ConfigDict

from typing import Optional


class CreateCompanyDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class ResponseCompanyDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    name: str

    created_at: str


class UpdateCompanyDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None