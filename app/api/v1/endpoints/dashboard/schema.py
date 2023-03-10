from datetime import date, datetime
from typing import List, Optional

from pydantic import Field, validator

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.utils import DropdownResponse


class OptionalNumberInfo(BaseSchema):
    number: Optional[str] = Field(..., description="Số")
    number_type: Optional[str] = Field(None, description="Loại số: Số TKTT/ SỐ GTDD")
    approval_status: int = Field(None, description="Trạng thái phê duyệt")

    @validator('approval_status', pre=True)
    def check_nullable(cls, value):
        return 0 if value is None else value


class TransactionListBusinessTypeResponse(BaseSchema):
    name: Optional[str] = Field(..., description="Tên loại nghiệp vụ")
    numbers: Optional[List[OptionalNumberInfo]] = Field(..., description="Số nghiệp vụ")


class TransactionListSenderResponse(BaseSchema):
    name: Optional[str] = Field(None, description="Tên người gửi")
    created_at: Optional[datetime] = Field(None, description="Ngày tạo")
    sla_time: Optional[str] = Field(None, description="Khoảng thời gian thực hiện")
    sla_deadline: Optional[int] = Field(None, description="Tình trạng SLA")


class TransactionListResponse(BaseSchema):
    created_at: datetime = Field(..., description="Thời gian tạo")
    cif_id: Optional[str] = Field(..., description="CIF ID")
    customer_cif_number: Optional[str] = Field(None, description="CIF number khách hàng")
    full_name_vn: Optional[str] = Field(None, description="Họ tên khách hàng")
    sender_cif_number: Optional[str] = Field(None, description="CIF number người làm giao dịch")
    sender_full_name_vn: Optional[str] = Field(None, description="Tên người làm giao dịch")
    booking_id: str = Field(..., description="Mã booking")
    booking_code: Optional[str] = Field(..., description="Mã booking")
    stage_role: Optional[str] = Field(..., description="Vai trò")
    status: Optional[str] = Field(..., description="Trạng thái")
    business_type: TransactionListBusinessTypeResponse = Field(..., description="Loại giao dịch")
    branch_code: Optional[str] = Field(..., description="Mã đơn vị kinh doanh")
    branch_name: Optional[str] = Field(..., description="Tên đơn vị kinh doanh")
    teller: TransactionListSenderResponse = Field(..., description="GDV")
    supervisor: TransactionListSenderResponse = Field(..., description="KSV")
    audit: TransactionListSenderResponse = Field(..., description="KSS")


class CustomerInfoResponse(BaseSchema):
    cif_id: str = Field(None, description="CIF id")
    cif_number: str = Field(None, description="CIF number")
    full_name: str = Field(None, description="Tên khách hàng")
    identity_number: str = Field(None, description="Giấy tờ định danh")
    phone_number: str = Field(None, description="Số điện thoại")
    street: str = Field(None, description="Số nhà - tên Đường")
    ward: DropdownResponse = Field(None, description="Phường - xã")
    district: DropdownResponse = Field(None, description="Quận - Huyện")
    province: DropdownResponse = Field(None, description="Tình thành")
    branch: DropdownResponse = Field(None, description="Chi nhánh")


class BranchResponse(BaseSchema):
    branch_code: str = Field(..., description="Mã chi nhánh")
    branch_name: str = Field(..., description="Tên chi nhánh")


class SelectDataForChardDashBoardRequest(BaseSchema):
    from_date: date = Field(..., description="Từ ngày")
    to_date: date = Field(..., description="Đến ngày")
    region_id: str = Field('ALL', description="Mã vùng")
    branch_code: str = Field('ALL', description="Mã chi nhánh")


class ListRegionResponse(BaseSchema):
    branch_id: str = Field(..., description="Mã vùng")
    branch_name: str = Field(..., description="Tên vùng")
    longitude: float = Field(..., description="Kinh độ")
    latitude: float = Field(..., description="Vĩ độ")
    type: str = Field(..., description="Loại")


class RegionResponse(BaseSchema):
    region_id: str = Field(..., description="ID Mã vùng")
    region_name: str = Field(..., description="Tên vùng")
    branches: List[ListRegionResponse] = Field(..., description="Chi nhánh")
    left: float = Field(..., description="Left")
    right: float = Field(..., description="Right")
    top: float = Field(..., description="Top")
    bottom: float = Field(..., description="Bottom")
