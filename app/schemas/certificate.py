from pydantic import BaseModel, ConfigDict


class CreateCertificateDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str



