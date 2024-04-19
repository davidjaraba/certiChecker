from pydantic import BaseModel, ConfigDict

from typing import Optional


class CreateCertificateDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class ResponseCertificateDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    name: str


class UpdateCertificateDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str]
