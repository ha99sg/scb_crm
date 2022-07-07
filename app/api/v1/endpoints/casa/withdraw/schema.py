from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from app.api.base.schema import BaseSchema, ResponseRequestSchema
from app.api.v1.schemas.utils import OptionalDropdownRequest


# II. Thông tin người hưởng thụ
class ReceiverInfoResponse(BaseSchema):
    withdraw_account_flag: bool = Field(
        ...,
        description='Cờ thông tin rút tiền , `true` = Rút tài khoản, `false` = Rút cheque'
    )
    currency: str = Field(..., description="Loại tiền")
    amount: int = Field(..., description="Số tiền")
    content: Optional[str] = Field(None, description="Nội dung rút tiền")


# III. Thông tin phí
class FeeInfoResponse(BaseSchema):
    is_transfer_payer: bool = Field(..., description="Cờ thu phí cùng giao dịch, `true` = Có, `false` = Không")
    payer: str = Field(..., description="Bên chuyển")
    fee_amount: int = Field(..., description="Số tiền phí")
    vat_tax: float = Field(..., description="Thuế VAT")
    total: float = Field(..., description="Tổng số tiền phí")
    actual_total: float = Field(..., description="Số tiền thực chuyển")


# A. Thông tin giao dịch
class TransactionResponse(BaseSchema):
    receiver_info_response: ReceiverInfoResponse = Field(..., description="Thông tin người hưởng thụ")
    fee_info_response: FeeInfoResponse = Field(..., description="Thông tin phí")


class DropdownCodeNameResponse(ResponseRequestSchema):
    code: Optional[str] = Field(..., description="Mã")
    name: Optional[str] = Field(..., description="Tên")


# I. Thông tin quản lý
class ManagementInfoResponse(BaseSchema):
    direct_staff: DropdownCodeNameResponse = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff: DropdownCodeNameResponse = Field(..., description="Mã nhân viên quản lý gián tiếp")


# II. Thông tin khách hàng giao dịch
class SenderInfoResponse(BaseSchema):
    cif_flag: bool = Field(
        ...,
        description="Cờ kiểm tra có CIF chưa, `true` = Có, `false` = Không"
    )
    cif_number: Optional[str] = Field(None, description="Mã khách hàng giao dịch")
    fullname_vn: Optional[str] = Field(None, description="Người giao dịch")
    identity: Optional[str] = Field(None, description="Giấy tờ định danh")
    issued_date: Optional[datetime] = Field(None, description="Ngày cấp")
    place_of_issue: Optional[str] = Field(None, description="Nơi cấp")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    mobile_phone: Optional[str] = Field(None, description="Điện thoại")
    note: Optional[str] = Field(None, description="Ghi chú")


# B. Thông tin khách hàng giao dịch
class TransactionalCustomerResponse(BaseSchema):
    management_info_response: ManagementInfoResponse = Field(..., description="I. Thông tin quản lý")
    sender_info_response: SenderInfoResponse = Field(..., description="II. Thông tin khách hàng giao dịch")


# Giao dịch rút tiền
class WithdrawResponse(BaseSchema):
    transaction_response: TransactionResponse = Field(..., description="Thông tin giao dịch")
    transactional_customer_response: TransactionalCustomerResponse = Field(..., description="Thông tin giao dịch")


########################################################################################################################

class CasaAccountsResponse(BaseSchema):
    number: str = Field(..., description="Tài khoản thanh toán")
    fullname_vn: str = Field(..., description="Tên chủ tài khoản")
    balance_available: int = Field(..., description="Số dư khả dụng")
    currency: str = Field(..., description="Loại tiền")
    account_type: str = Field(..., description="Loại tài khoản")


# Danh sách tài khoản nguồn
class SourceAccountInfoResponse(BaseSchema):
    casa_accounts: List[CasaAccountsResponse] = Field(..., description="Tài khoản nguồn")
    total_items: int = Field(..., description="Tổng số tài khoản")


########################################################################################################################
# Request
########################################################################################################################
# I.Tài khoản  nguồn
class SourceAccountRequest(BaseSchema):
    account_num: str = Field(..., description="Số tài khoản")


# II. Thông tin người hưởng thụ
class ReceiverInfoRequest(BaseSchema):
    withdraw_account_flag: bool = Field(
        ...,
        description='Cờ thông tin rút tiền , `true` = Rút tài khoản, `false` = Rút cheque'
    )
    amount: int = Field(..., description="2. Số tiền")
    seri_cheque: OptionalDropdownRequest = Field(None, description="3. Seri Cheque")
    date_of_issue: Optional[date] = Field(None, description="4. Ngày ký phát")
    exchange_VND_flag: Optional[int] = Field(None, description='5. Quy đổi VND')
    exchange_rate: Optional[int] = Field(None, description="6. Tỉ giá")
    exchanged_money_VND: Optional[int] = Field(None, description="7. Số tiền quy đổi VND")
    reciprocal_rate_headquarters: Optional[int] = Field(None, description="8. Tỷ giá đối ứng hội sở")
    content: str = Field(..., description="9. Nội dung rút tiền")


# III. Thông tin phí
class FeeInfoRequest(BaseSchema):
    is_transfer_payer: bool = Field(
        ...,
        description=' 1. Cờ có thu phí hay không, `true`: Có thu phí, `false` = Không thu phí'
    )
    payer: Optional[str] = Field(None, description="Bên thanh toán phí")
    fee_amount: Optional[int] = Field(None, description="3. Số tiền phí")


# A. THÔNG TIN GIAO DỊCH
class TransactionInfoRequest(BaseSchema):
    source_accounts: SourceAccountRequest = Field(..., description="I. Tài khoản nguồn")
    receiver_info: ReceiverInfoRequest = Field(..., description="II. Thông tin người hưởng thụ")
    fee_info: Optional[FeeInfoRequest] = Field(..., description="III. Thông tin phí")


# I. Thông tin quản lý
class ManagementInfoRequest(BaseSchema):
    direct_staff_code: Optional[str] = Field(..., description="Mã nhân viên kinh doanh")
    indirect_staff_code: Optional[str] = Field(..., description="Mã nhân viên quản lý gián tiếp")


# II. Thông tin khách hàng giao dịch
class SenderInfoRequest(BaseSchema):
    cif_flag: bool = Field(..., description="Cờ có CIF chưa, `true` = Có CIF, `false` = Chưa có CIF")
    cif_number: Optional[str] = Field(None, description="Số CIF")
    fullname_vn: Optional[str] = Field(None, description="Người giao dịch")
    identity: Optional[str] = Field(None, description="Thông tin giấy tờ định danh")
    issued_date: Optional[date] = Field(None, description="Ngày cấp")
    place_of_issue: Optional[str] = Field(None, description="Nơi cấp")
    address_full: Optional[str] = Field(None, description="Địa chỉ")
    mobile_phone: Optional[str] = Field(None, description="SĐT")
    telephone: Optional[str] = Field(None, description="SĐT")
    otherphone: Optional[str] = Field(None, description="SĐT")
    note: Optional[str] = Field(None, description="Ghi chú")


# B. THÔNG TIN KHÁCH HÀNG GIAO DỊCH
class CustomerInfoRequest(BaseSchema):
    management_info: ManagementInfoRequest = Field(..., description="I. Thông tin quản lý")
    sender_info: SenderInfoRequest = \
        Field(..., description="II. Thông tin khách hàng giao dịch")


# Giao dịch rút tiền
class WithdrawRequest(BaseSchema):
    transaction_info: TransactionInfoRequest = Field(..., description="A. Thông tin giao dịch")
    customer_info: CustomerInfoRequest = Field(..., description="B. Thông tin khách hàng giao dịch")
