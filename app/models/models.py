from typing import List
from sqlalchemy import Column, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = 'companies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    urls: Mapped[List["URL"]] = relationship(back_populates='company', cascade='all, delete')
    companycertificates: Mapped[List["CompanyCertificate"]] = relationship(back_populates='company',
                                                                           cascade='all, delete')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Company(id={self.id!r}, name={self.name!r}, urls={self.urls!r})"


class Certificate(Base):
    __tablename__ = 'certificates'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    companycertificates: Mapped[List["CompanyCertificate"]] = relationship(back_populates='certificate', cascade='all')

    def __repr__(self) -> str:
        return f"Certificate(name={self.name!r}"


class URL(Base):
    __tablename__ = 'urls'
    url: Mapped[str] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), nullable=False)
    company: Mapped["Company"] = relationship(back_populates="urls")
    resources: Mapped[List["Resource"]] = relationship(back_populates='url', cascade='all, delete')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"URL(company_id={self.company_id!r}, company={self}"


class Resource(Base):
    __tablename__ = 'resources'
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    type: Mapped[str] = mapped_column(String(), nullable=False)
    full_url: Mapped[str] = mapped_column(String(255), nullable=False)
    url_id: Mapped[str] = mapped_column(ForeignKey('urls.url'), nullable=False)
    url: Mapped[URL] = relationship(back_populates="resources")
    certificate: Mapped["CompanyCertificate"] = relationship(back_populates="resource")
    path_file: Mapped[str] = mapped_column(String(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"URL()"


class CompanyCertificate(Base):
    __tablename__ = 'companycertificates'
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), primary_key=True)
    company: Mapped["Company"] = relationship(back_populates="companycertificates")
    certificate_id: Mapped[int] = mapped_column(ForeignKey('certificates.id'), primary_key=True)
    certificate: Mapped["Certificate"] = relationship(back_populates="companycertificates")
    found_date = Column(DateTime(timezone=True), server_default=func.now(), primary_key=True)
    removed_date = Column(DateTime(timezone=True))

    # created_at = Column(DateTime(timezone=True), server_default=func.now())

    resource_id: Mapped[str] = mapped_column(ForeignKey('resources.id'))
    resource: Mapped[Resource] = relationship(back_populates='certificate')

    def __repr__(self) -> str:
        return f"CompanyCertificate(company_id={self.company_id}, certificate_name={self.certificate.certificate_name if self.certificate else 'Unknown'}, found_date={self.found_date}, resource_id={self.resource_id})"