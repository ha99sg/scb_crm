from fastapi import APIRouter, Header, Path

from app.api.base.schema import ResponseData
from app.api.v1.endpoints.approval_v2.template.controller import (
    CtrTemplateDetail
)

router = APIRouter()


@router.get(
    path="/{template_id}/",
    name="Thông tin Biểu Mẫu",
    description="Thông tin Biểu Mẫu",
)
async def view_form(
        booking_id: str = Header(..., description="Mã phiên giao dịch"),
        template_id: str = Path(..., description='id template version 1'),
        # current_user=Depends(get_current_user_from_header())
):
    template_detail_info = await CtrTemplateDetail().ctr_get_template_detail(
        template_id=template_id,
        booking_id=booking_id
    )
    return ResponseData(**template_detail_info)