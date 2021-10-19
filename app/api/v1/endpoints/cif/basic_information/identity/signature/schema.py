from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema


class SignaturesResponse(BaseSchema):
    date: str = Field(..., description='Ngày tạo')
    identity_image_transaction_1: str = Field(..., description='Hình ảnh định danh chữ ký khách hàng')
    identity_image_transaction_2: str = Field(..., description='Hình ảnh định danh chữ ký khách hàng')
    checked_flag: bool = Field(..., description='Trạng thái hoạt động')


class CompareSignaturesResponse(BaseSchema):
    compare_image_url: str = Field(..., description='Hình ảnh đối chiếu')
    similar_percent: int = Field(..., description='Số phần trăm đối chiếu')


class SignaturesSuccessResponse(BaseSchema):
    customer_signatures: List[SignaturesResponse] = Field(..., description='Mẫu chữ ký')
    compare_signature: CompareSignaturesResponse = Field(..., description='Chữ ký kiểm tra sự tương đồng')
