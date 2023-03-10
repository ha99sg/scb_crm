from fastapi import APIRouter, Depends, Header
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.approval.face.controller import CtrApproveFace
from app.api.v1.endpoints.approval.face.schema import (
    ApprovalFaceRequest, ApprovalFaceSuccessResponse
)

router = APIRouter()


@router.post(
    path="/face/",
    description="[Thông tin xác thực] Upload khuôn mặt",
    name="So sánh khuôn mặt",
    responses=swagger_response(
        response_model=ResponseData[ApprovalFaceSuccessResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_upload_face(
        BOOKING_ID: str = Header(..., description="Mã phiên giao dịch"),  # noqa
        request: ApprovalFaceRequest = Depends(ApprovalFaceRequest.get_upload_request),
):
    cif_id, image_file, amount, current_user = request
    approve_info = await CtrApproveFace(current_user).ctr_upload_face(
        cif_id=cif_id,
        image_file=image_file,
        amount=amount,
        booking_id=BOOKING_ID
    )

    return ResponseData[ApprovalFaceSuccessResponse](**approve_info)
