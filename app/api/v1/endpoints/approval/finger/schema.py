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
    hand_side_left: List[FingerBase] = Field(..., description='Mẫu vân tay 1')
    hand_side_right: List[FingerBase] = Field(..., description='Mẫu vân tay 2')
