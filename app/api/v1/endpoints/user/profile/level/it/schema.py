from typing import Optional, Union

from pydantic import Field

from app.api.base.schema import BaseSchema


# Thông tin trình độ tin học
class ITLevelInfoResponse(BaseSchema):
    certification: Optional[str] = Field(..., description="Chứng chỉ")
    level: Optional[str] = Field(..., description="Trình độ")
    gpa: Optional[Union[int, str]] = Field(None, description="Điểm số/Xếp loại")
