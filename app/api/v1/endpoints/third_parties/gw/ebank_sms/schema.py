from datetime import date
from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema

# GW selectMobileNumberSMSByAccountCASA


class SelectMobileNumberSMSByAccountCASAEbankSMSInfoRequest(BaseSchema):
    ebank_sms_indentify_num: str = Field(..., description="Số tài khoản thanh toán", example="1380104914870005")


class GWSelectMobileNumberSMSByAccountCASARequest(BaseSchema):
    ebank_sms_info: SelectMobileNumberSMSByAccountCASAEbankSMSInfoRequest


class SelectMobileNumberSMSByAccountCASAEbankSMSInfoItemBranchInfoResponse(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị đăng ký dịch vụ", example="")
    branch_name_vn: str = Field(..., description="Tên đơn vị đăng ký dịch vụ", example="")


class SelectMobileNumberSMSByAccountCASAEbankSMSInfoItemResponse(BaseSchema):
    ebank_sms_indentify_num: str = Field(..., description="Số điện thoại", example="")
    ebank_sms_full_name: str = Field(..., description="Họ và tên", example="")
    ebank_sms_owner_phone: str = Field(..., description="Loại số điện thoại: Chính chủ: 'Y', người thân: 'N'",
                                       example="")
    ebank_sms_relations: str = Field(..., description="Mối quan hệ với số điện thoại chính. VD: Bố mẹ, Vợ chồng",
                                     example="")
    ebank_sms_reg_date: date = Field(..., description="Ngày đăng ký", example="")
    ebank_sms_status: str = Field(..., description="Trạng thái hoạt động", example="")
    branch_info: SelectMobileNumberSMSByAccountCASAEbankSMSInfoItemBranchInfoResponse


class SelectMobileNumberSMSByAccountCASAEbankSMSInfoListResponse(BaseSchema):
    ebank_sms_info_item: SelectMobileNumberSMSByAccountCASAEbankSMSInfoItemResponse


class GWSelectMobileNumberSMSByAccountCASAResponse(BaseSchema):
    ebank_sms_info_list: List[SelectMobileNumberSMSByAccountCASAEbankSMSInfoListResponse]


########################################################################################################################

# selectAccountTDByMobileNum

class SelectAccountTDByMobileNumEbankSMSInfoRequest(BaseSchema):
    ebank_sms_indentify_num: str = Field(..., description="Số điện thoại đăng ký sms cho các tài khoản tiết kiệm",
                                         example="0903107036")


class SelectAccountTDByMobileNumRequest(BaseSchema):
    ebank_sms_info: SelectAccountTDByMobileNumEbankSMSInfoRequest


class SelectAccountTDByMobileNumEbankSMSInfoItemBranchInfoResponse(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị đăng ký dịch vụ")
    branch_name_vn: str = Field(..., description="Tên đơn vị đăng ký dịch vụ")


class SelectAccountTDByMobileNumEbankSMSInfoItemResponse(BaseSchema):
    ebank_sms_indentify_num: str = Field(..., description="Số tải khoản tiết kiệm sử dụng dịch vụ SMS")
    ebank_sms_full_name: str = Field(..., description="Họ và tên khách hàng")
    ebank_sms_reg_date: date = Field(..., description="Ngày đăng ký")
    ebank_sms_status: str = Field(..., description="Trạng thái hoạt động")
    branch_info: SelectAccountTDByMobileNumEbankSMSInfoItemBranchInfoResponse


class SelectAccountTDByMobileNumEbankSMSInfoListResponse(BaseSchema):
    ebank_sms_info_item: SelectAccountTDByMobileNumEbankSMSInfoItemResponse


class SelectAccountTDByMobileNumResponse(BaseSchema):
    ebank_sms_info_list: List[SelectAccountTDByMobileNumEbankSMSInfoListResponse]

########################################################################################################################

# registerSMSServiceByAccountCASA


class RegisterSmsServiceByAccountCasaAccountInfoRequest(BaseSchema):
    account_num: str = Field(..., description="Số tài khoản thanh toán", example="112233445566")
    account_type: str = Field(..., description="Giá trị TT : Đăng ký biến động số dư"
                                               " Giá trị TK: Đăng ký SMS tiết kiệm", example="TT")


class RegisterSmsServiceByAccountCasaEbankSmsInfoItemCIFInfoRequest(BaseSchema):
    cif_num: str = Field(..., description="Số CIF")


class RegisterSmsServiceByAccountCasaEbankSmsInfoItemBranchInfoRequest(BaseSchema):
    branch_code: str = Field(..., description="Mã đơn vị đăng ký dịch vụ SMS Banking", example="000")


class RegisterSmsServiceByAccountCasaEbankSmsInfoChildItemRequest(BaseSchema):
    ebank_sms_indentify_num: str = Field(...,
                                         description="Số điện thoại đăng ký sử dụng dịch vụ SMS Banking",
                                         example="0909111222")
    cif_info: RegisterSmsServiceByAccountCasaEbankSmsInfoItemCIFInfoRequest
    branch_info: RegisterSmsServiceByAccountCasaEbankSmsInfoItemBranchInfoRequest


class RegisterSmsServiceByAccountCasaEbankSmsInfoItemRequest(BaseSchema):
    ebank_sms_info_item: RegisterSmsServiceByAccountCasaEbankSmsInfoChildItemRequest


class RegisterSmsServiceByAccountCasaStaffInfoCheckerRequest(BaseSchema):
    staff_name: str = Field(..., description="Kiểm soát viên", example="HOANT2")


class RegisterSmsServiceByAccountCasaStaffInfoMakerRequest(BaseSchema):
    staff_name: str = Field(..., description="Giao dịch viên", example="KHANHLQ")


class RegisterSmsServiceByAccountCasaRequest(BaseSchema):
    account_info: RegisterSmsServiceByAccountCasaAccountInfoRequest
    ebank_sms_info_list: List[RegisterSmsServiceByAccountCasaEbankSmsInfoItemRequest]
    staff_info_checker: RegisterSmsServiceByAccountCasaStaffInfoCheckerRequest
    staff_info_maker: RegisterSmsServiceByAccountCasaStaffInfoMakerRequest
