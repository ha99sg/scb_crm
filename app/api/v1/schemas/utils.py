from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


class DropdownResponse(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh`')
    code: str = Field(..., description='`Mã`')
    name: str = Field(..., description='`Tên`')


class OptionalDropdownResponse(BaseSchema):
    id: Optional[str] = Field(..., description='`Chuỗi định danh`')
    code: Optional[str] = Field(..., description='`Mã`')
    name: Optional[str] = Field(..., description='`Tên`')


class DropdownRequest(BaseSchema):
    id: str = Field(..., description='`Chuỗi định danh`')
