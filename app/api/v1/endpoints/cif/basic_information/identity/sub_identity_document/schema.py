from datetime import date
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownRequest, DropdownResponse


########################################################################################################################
# Response
########################################################################################################################
# Response Chi tiết GTĐD phụ -> Phân tích OCR
class SubIdentityOCRResultResponse(BaseSchema):
    sub_identity_number: str = Field(..., min_length=1, description="Số GTĐD")
    symbol: str = Field(None, min_length=1, description="Ký hiệu")
    full_name_vn: str = Field(..., min_length=1, description="Họ và tên")
    date_of_birth: date = Field(..., description="Ngày sinh")
    passport_number: str = Field(..., min_length=1, description="Số hộ chiếu")
    place_of_issue: DropdownResponse = Field(..., description="Nơi cấp")
    expired_date: date = Field(..., description="Có giá trị đến")
    issued_date: date = Field(..., description="Ngày cấp")


# Response Chi tiết GTĐD phụ
class SubIdentityDetailResponse(BaseSchema):
    id: str = Field(..., min_length=1, description="ID GTĐD phụ")
    name: str = Field(..., min_length=1, description="Tên GTĐD phụ")
    sub_identity_document_type: DropdownResponse = Field(..., description="Loại GTĐD phụ")
    sub_identity_document_image_url: str = Field(..., min_length=1, description="I. Thông tin giấy tờ")
    ocr_result: SubIdentityOCRResultResponse = Field(..., description="II. Phân tích OCR")


# Hình ảnh trong lịch sử
class IdentityImage(BaseSchema):
    image_url: str = Field(..., min_length=1, description="URL hình ảnh định danh")


# Lịch sử thay đổi giấy tờ định danh phụ
class LogResponse(BaseSchema):
    reference_flag: bool = Field(..., description="Cờ giấy tờ định danh phụ dùng để so sánh với hình gốc")
    created_date: date = Field(..., description="Ngày ghi log")
    identity_images: List[IdentityImage] = Field(..., description="Danh sách hình ảnh")


########################################################################################################################
# Request
########################################################################################################################
# Request Body Lưu GTĐD phụ -> Phân tích OCR
class SubIdentityOCRResultRequest(SubIdentityOCRResultResponse):
    place_of_issue: DropdownRequest = Field(..., description="Nơi cấp")


# Request Body Lưu GTĐD phụ
class SubIdentityDocumentRequest(BaseSchema):
    id: Optional[str] = Field(..., min_length=1, description="ID GTĐD phụ, nếu có gửi lên id là chỉnh sửa, không gửi "
                                                             "lên id là tạo mới, những id có tồn tại trong hệ thống "
                                                             "nhưng không gửi lên là bị xóa")
    name: str = Field(..., min_length=1, description="Tên GTĐD phụ")
    sub_identity_document_image_url: str = Field(..., min_length=1, description="I. Thông tin giấy tờ")
    sub_identity_document_type: DropdownRequest = Field(..., description="Loại GTĐD phụ")
    ocr_result: SubIdentityOCRResultRequest = Field(..., description="II. Phân tích OCR")
