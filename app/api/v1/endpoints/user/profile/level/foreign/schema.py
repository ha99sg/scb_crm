from datetime import date
from typing import Optional

from pydantic import Field

from app.api.base.schema import BaseSchema


# Thông tin trình độ ngoại ngữ
class ForeignLanguageLevelInfoResponse(BaseSchema):
    language_type: Optional[str] = Field(..., description="Ngoại ngữ")
    level: Optional[str] = Field(..., description="Trình độ")
    gpa: Optional[str] = Field(..., description="Điểm")
    certification_date: Optional[date] = Field(..., description="Ngày nhận chứng chỉ")
