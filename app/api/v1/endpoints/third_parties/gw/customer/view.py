from fastapi import APIRouter, Body, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.base_field import CustomField
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.endpoints.third_parties.gw.customer.example import (
    CUSTOMER_CHECK_EXIST_CIF_ID_FAIL_EXAMPLE,
    CUSTOMER_CHECK_EXIST_CIF_ID_SUCCESS_EXAMPLE, CUSTOMER_CIF_ID,
    CUSTOMER_INFO_DETAIL_SUCCESS_EXAMPLE, CUSTOMER_INFO_LIST_SUCCESS_EXAMPLE
)
from app.api.v1.endpoints.third_parties.gw.customer.schema import (
    CustomerInfoListCIFRequest, GWCustomerCheckExistRequest,
    GWCustomerCheckExistResponse, GWCustomerInfoDetailResponse,
    GWCustomerInfoListResponse
)

router = APIRouter()


@router.post(
    path="/",
    name="[GW] Lấy thông tin khách hàng",
    description="[GW] Lấy thông tin khách hàng CIF/CMND/CCCD/Số điện thoại/Họ tên KH",
    responses=swagger_response(
        response_model=ResponseData[GWCustomerInfoListResponse],
        success_examples=CUSTOMER_INFO_LIST_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_customer_info_list(
        request: CustomerInfoListCIFRequest = Body(..., example=CUSTOMER_CIF_ID),
        current_user=Depends(get_current_user_from_header())
):
    gw_customer_info_list = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_list(
        cif_number=request.cif_number
    )

    return ResponseData[GWCustomerInfoListResponse](**gw_customer_info_list)


@router.post(
    path="/check-exist/",
    name="[GW] Kiểm tra số CIF có tồn tại không",
    description="[GW] Kiểm tra số CIF tự chọn có tồn tại trên CoreFCC",
    responses=swagger_response(
        response_model=ResponseData[GWCustomerCheckExistResponse],
        success_examples=CUSTOMER_CHECK_EXIST_CIF_ID_SUCCESS_EXAMPLE,
        fail_examples=CUSTOMER_CHECK_EXIST_CIF_ID_FAIL_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_check_exist_casa_account_info(
        request: GWCustomerCheckExistRequest = Body(..., example=CUSTOMER_CIF_ID),
        current_user=Depends(get_current_user_from_header())
):
    gw_check_exist_casa_account_info = await CtrGWCustomer(current_user).ctr_gw_check_exist_customer_detail_info(
        cif_number=request.cif_number
    )
    return ResponseData[GWCustomerCheckExistResponse](**gw_check_exist_casa_account_info)


@router.post(
    path="/{cif_number}/",
    name="[GW] Lấy chi tiết thông tin khách hàng",
    description="Lấy chi tiết thông tin khách hàng theo CIF",
    responses=swagger_response(
        response_model=ResponseData[GWCustomerInfoDetailResponse],
        success_examples=CUSTOMER_INFO_DETAIL_SUCCESS_EXAMPLE,
        success_status_code=status.HTTP_200_OK
    )
)
async def view_gw_get_customer_info_detail(
    cif_number: str = CustomField().CIFNumberPath,
    current_user=Depends(get_current_user_from_header())
):
    gw_customer_info_detail = await CtrGWCustomer(current_user).ctr_gw_get_customer_info_detail(
        cif_number=cif_number
    )
    return ResponseData[GWCustomerInfoDetailResponse](**gw_customer_info_detail)
