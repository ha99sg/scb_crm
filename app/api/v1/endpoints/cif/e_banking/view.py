from typing import List

from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.e_banking.controller import CtrEBanking
from app.api.v1.endpoints.cif.e_banking.schema import (
    EBankingRequest, EBankingResponse, ListBalancePaymentAccountResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse

router = APIRouter()


@router.post(
    path="/",
    name="E-banking",
    description="Tạo dữ liệu tab `E BANKING` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_save_e_banking(
        e_banking: EBankingRequest,
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    e_banking_data = await CtrEBanking(current_user).ctr_save_e_banking(cif_id, e_banking)
    return ResponseData[SaveSuccessResponse](**e_banking_data)


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
    path="/balance-payment-account",
    name="Danh sách tài khoản thanh toán",
    description="Lấy dữ liệu tab `DANH SÁCH TÀI KHOẢN THANH TOÁN`",
    responses=swagger_response(
        response_model=ResponseData[List[ListBalancePaymentAccountResponse]],
        success_status_code=status.HTTP_200_OK
    ),
)
async def view_balance_payment_account(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    balance_payment_account_data = await CtrEBanking(current_user).ctr_balance_payment_account(cif_id)
    return ResponseData[List[ListBalancePaymentAccountResponse]](**balance_payment_account_data)
