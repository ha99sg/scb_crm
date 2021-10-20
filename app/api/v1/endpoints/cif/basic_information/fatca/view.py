from fastapi import APIRouter, Depends, Path
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.fatca.controller import (
    CtrFatca
)
from app.api.v1.endpoints.cif.basic_information.fatca.schema import (
    FatcaResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="1. TTCN - Thông tin FATCA",
    description="Lấy dữ liệu tab `CHỮ KÝ` của khách hàng",
    responses=swagger_response(
        response_model=ResponseData[FatcaResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_retrieve_fatca(
        cif_id: str = Path(...),
        current_user=Depends(get_current_user_from_header())
):
    fatca_data = await CtrFatca(current_user).ctr_get_fatca(cif_id)
    return ResponseData[FatcaResponse](**fatca_data)
