from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.e_banking.controller import CtrEBanking
from app.api.v1.endpoints.cif.e_banking.schema import (
    EBankingResponse, ResetPasswordEBankingResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="E-banking",
    description="Lấy dữ liệu tab `E BANKING` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[EBankingResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_retrieve_e_banking(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_data = await CtrEBanking(current_user).ctr_e_banking(cif_id)
    return ResponseData[EBankingResponse](**e_banking_data)


@router.get(
    path="/reset-password/",
    name="Detail Reset Password",
    description="Chi tiết IV. E-Banking - Cấp lại mật khẩu E-Banking call center",
    responses=swagger_response(
        response_model=ResponseData[ResetPasswordEBankingResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail_reset_password(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_e_banking = CtrEBanking(current_user)

    e_banking_data = await ctr_e_banking.get_detail_reset_password(cif_id=cif_id)

    return ResponseData[ResetPasswordEBankingResponse](**e_banking_data)
