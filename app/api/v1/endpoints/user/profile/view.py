from fastapi import APIRouter, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.endpoints.user.profile.controller import CtrProfile
from app.api.v1.endpoints.user.profile.schema import ProfileResponse

router = APIRouter()


@router.get(
    path="/",
    name="Thông tin chi tiết nhân viên",
    description="Thông tin chi tiết nhân viên",
    responses=swagger_response(
        response_model=ResponseData[ProfileResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_profile(
        employee_id: str = Query(..., description="employee_id")
):
    profile_info = await CtrProfile().ctr_profile(employee_id=employee_id)
    return ResponseData[ProfileResponse](**profile_info)
