from datetime import datetime

from pydantic import Field

from app.api.base.schema import BaseSchema


# Schema upload file response DMS
class FileBDSServiceRes(BaseSchema):
    created_at: datetime = Field(None)
    created_by: str = Field(None)
    updated_at: datetime = Field(None)
    updated_by: str = Field(None)
    type: int = Field(None)
    uuid: str = Field(...)
    name: str = Field(...)
    content_type: str = Field(...)
    size: int = Field(None)
    version: float = Field(None)


class FileBDSServiceReq:
    uuid: str = Field(...)


class FileRes(BaseSchema):
    file_id: int = Field(None)
    uuid: str = Field(None)
    type: str = Field(None)  # FILE_EXTENSION
    display_order: int = Field(None)
    description: str = Field(None)
    content_type: str = Field(None)
    create_by: datetime = Field(None)
    create_at: datetime = Field(None)


class FileDBSServiceDownloadRes(BaseSchema):
    uuid: str = Field(...)
    file_url: str = Field(...)
    file_name: str = Field(...)


class CheckFileRes(BaseSchema):
    uuid: str
    is_exist: bool
