from datetime import datetime

from pydantic import Field

from app.api.v1.schemas.base import CustomBaseModel


# chi nhánh ngân hàng
class BranchRes(CustomBaseModel):
    branch_code: str
    branch_name: str
    branch_address: str
    branch_parent_code: str
    branch_tax_code: str
    branch_phone: str
    branch_status: str
    branch_region_code: str
    branch_region_name: str


# Schema upload file response DMS
class FileBDSServiceRes(CustomBaseModel):
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


class FileRes(CustomBaseModel):
    file_id: int = Field(None)
    uuid: str = Field(None)
    type: str = Field(None)  # FILE_EXTENSION
    display_order: int = Field(None)
    description: str = Field(None)
    content_type: str = Field(None)
    create_by: datetime = Field(None)
    create_at: datetime = Field(None)


class FileDBSServiceDownloadRes(CustomBaseModel):
    uuid: str = Field(...)
    file_url: str = Field(...)
    file_name: str = Field(...)


class CheckFileRes(CustomBaseModel):
    uuid: str
    is_exist: bool
