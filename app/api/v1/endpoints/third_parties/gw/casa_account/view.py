from fastapi import APIRouter, Body, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.third_parties.gw.casa_account.controller import (
    CtrGWCasaAccount
)
from app.api.v1.endpoints.third_parties.gw.casa_account.schema import (
    GWCasaAccountByCIFNumberRequest, GWCasaAccountByCIFNumberResponse,
    GWCasaAccountCheckExistRequest, GWCasaAccountCheckExistResponse,
    GWCasaAccountResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Danh sách Tài Khoản thanh toán theo số CIF",
    description="[GW] Tìm kiếm danh sách Tài Khoản thanh toán theo số CIF",
    responses=swagger_response(
        response_model=ResponseData[GWCasaAccountByCIFNumberResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_casa_account_by_cif_number(
        request: GWCasaAccountByCIFNumberRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    customer_information = await CtrGWCasaAccount(current_user).ctr_gw_get_casa_account_by_cif_number(
        cif_number=request.cif_number
    )
    return ResponseData[GWCasaAccountByCIFNumberResponse](**customer_information)


@router.post(
    path="/check-exist/",
    name="[GW] Kiểm tra số TK có tồn tại không",
    description="[GW] Kiểm tra số TK thanh toán tự chọn có tồn tại trên CoreFCC",
    responses=swagger_response(
        response_model=ResponseData[GWCasaAccountCheckExistResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_check_exist_casa_account_info(
        request: GWCasaAccountCheckExistRequest = Body(...),
        current_user=Depends(get_current_user_from_header())
):
    gw_check_exist_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_check_exist_casa_account_info(
        account_number=request.account_number
    )
    return ResponseData[GWCasaAccountCheckExistResponse](**gw_check_exist_casa_account_info)


@router.post(
    path="/{account_number}/",
    name="[GW] Chi tiết tài khoản thanh toán",
    description="[GW] Lấy chi tiết tài Khoản thanh toán theo số tài khoản",
    responses=swagger_response(
        response_model=ResponseData[GWCasaAccountResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_casa_account_info(
        account_number: str = Path(..., description="Số tài khoản"),
        current_user=Depends(get_current_user_from_header())
):
    gw_casa_account_info = await CtrGWCasaAccount(current_user).ctr_gw_get_casa_account_info(
        account_number=account_number
    )
    return ResponseData[GWCasaAccountResponse](**gw_casa_account_info)
