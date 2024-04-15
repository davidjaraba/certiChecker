import datetime
from os import path
from typing import List, Dict
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import QueryableAttribute
import json


class Base(DeclarativeBase):
    pass




class Company(Base):
    __tablename__ = 'companies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    urls: Mapped[List["URL"]] = relationship(back_populates='company', cascade='all, delete')
    companycertificates: Mapped[List["CompanyCertificate"]] = relationship(back_populates='company', cascade='all, delete')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Company(id={self.id!r}, name={self.name!r}"


class Certificate(Base):
    __tablename__ = 'certificates'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    companycertificates: Mapped[List["CompanyCertificate"]] = relationship(back_populates='certificate', cascade='all')

    def __repr__(self) -> str:
        return f"Certificate(name={self.name!r}"

    def as_dict(self)-> Dict:
        return {}


class URL(Base):
    __tablename__ = 'urls'
    url: Mapped[str] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))
    company: Mapped["Company"] = relationship(back_populates="urls")
    resources: Mapped[List["Resource"]] = relationship(back_populates='url', cascade='all, delete')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"URL(company_id={self.company_id!r}, company={self}"


class Resource(Base):
    __tablename__ = 'resources'
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    type: Mapped[str] = mapped_column(String())
    url_id: Mapped[str] = mapped_column(ForeignKey('urls.url'))
    url: Mapped[URL] = relationship(back_populates="resources")
    certificate: Mapped["CompanyCertificate"] = relationship(back_populates="resource")
    path_file: Mapped[str] = mapped_column(String())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"URL()"


class CompanyCertificate(Base):
    __tablename__ = 'companycertificates'
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'),primary_key=True)
    company: Mapped["Company"] = relationship(back_populates="companycertificates")
    certificate_id: Mapped[int] = mapped_column(ForeignKey('certificates.id'),primary_key=True)
    certificate: Mapped["Certificate"] = relationship(back_populates="companycertificates")
    found_date = Column(DateTime(timezone=True), server_default=func.now(), primary_key=True)
    removed_date = Column(DateTime(timezone=True))

    # created_at = Column(DateTime(timezone=True), server_default=func.now())

    resource_id: Mapped[str] = mapped_column(ForeignKey('resources.id'))
    resource: Mapped[Resource] = relationship(back_populates='certificate')
