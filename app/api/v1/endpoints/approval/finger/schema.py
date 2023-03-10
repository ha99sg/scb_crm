from datetime import datetime
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest


class FingerBase(BaseSchema):
    image_id: str = Field(..., description='id')
    image_url: str = Field(..., description='Ảnh vân tay')
    make_at: datetime = Field(..., description='Thời gian')
    finger_type: DropdownRequest = Field(..., description='Loại ngón tay')
    hand_side: DropdownRequest = Field(..., description='Loại bàn tay')


class FingersResponse(BaseSchema):
    left_hand: List[FingerBase] = Field(..., description='Mẫu vân tay trái')
    right_hand: List[FingerBase] = Field(..., description='Mẫu vân tay phải')


class CompareFingerPrintRequest(BaseSchema):
    uuid: str = Field(..., description='uuid upload file')
    uuid_ekyc: str = Field(..., description='uuid_ekyc upload file')


class CompareFingerPrintResponse(BaseSchema):
    image_url: str = Field(..., description='image url')
    similarity_percent: int = Field(..., description="Tỷ lệ phần trăm giống nhau")
    uuid: str = Field(..., description='uuid upload service file')
