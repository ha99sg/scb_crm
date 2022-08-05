from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import EmailStr
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.email.controller import CtrGWEmail

router = APIRouter()


@router.post(
    path="/sendEmail",
    name="[GW] Send Email",
    description="[GW] Gửi Email",
    responses=swagger_response(
        response_model=None,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_register_sms_service_by_mobile_number(
        current_user=Depends(get_current_user_from_header()),
        data_input__product_code: str = Form(..., alias="sendEmail_in.data_input.product_code",
                                             description="Mã chương trình -> Để chọn đúng SMTP config"),
        data_input__email_to: Optional[EmailStr] = Form(..., alias="sendEmail_in.data_input.email_to",
                                                        description="Địa chỉ email cần gửi, cần gửi tới nhiều người"
                                                                    " thì gửi lên nhiều key này,"
                                                                    " không có thì không gửi lên"),
        data_input__email_cc: Optional[EmailStr] = Form(..., alias="sendEmail_in.data_input.email_cc",
                                                        description="Địa chỉ email cần cc, cần gửi tới nhiều "
                                                                    "người thì gửi lên nhiều key này,"
                                                                    " không có thì không gửi lên"),
        data_input__email_bcc: Optional[EmailStr] = Form(..., alias="sendEmail_in.data_input.email_bcc",
                                                         description="Địa chỉ email cần bcc, cần gửi tới nhiều"
                                                                     " người thì gửi lên nhiều key này,"
                                                                     " không có thì không gửi lên"),
        data_input__email_subject: str = Form(..., alias="sendEmail_in.data_input.email_subject",
                                              description="Tiêu đề"),
        data_input__email_content_html: str = Form(..., alias="sendEmail_in.data_input.email_content_html",
                                                   description="Nội dung HTML"),
        data_input__email_attachment_file: Optional[UploadFile] = File(...,
                                                                       alias="sendEmail_in.data_input.email_attachment_file",
                                                                       description="Tệp đính kèm, cần gửi nhiều file thì gửi lên nhiều key này, không có thì không gửi lên"),
):
    ctr_send_email = await CtrGWEmail(
        current_user).ctr_gw_send_email(
        product_code=data_input__product_code,
        list_email_to=data_input__email_to,
        list_email_cc=data_input__email_cc,
        list_email_bcc=data_input__email_bcc,
        email_subject=data_input__email_subject,
        email_content_html=data_input__email_content_html,
        list_email_attachment_file=data_input__email_attachment_file,
    )

    ctr_send_email['data'] = None

    return ResponseData(**ctr_send_email)
