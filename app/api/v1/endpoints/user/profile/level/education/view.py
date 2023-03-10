from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.level.education.controller import (
    CtrEducation
)
from app.api.v1.endpoints.user.profile.level.education.schema import (
    EducationLevelInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN TRÌNH ĐỘ] - A. TRÌNH ĐỘ VĂN HÓA",
    description="[THÔNG TIN TRÌNH ĐỘ] - A. TRÌNH ĐỘ VĂN HÓA",
    responses=swagger_response(
        response_model=ResponseData[EducationLevelInfoResponse],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_education(
        current_user=Depends(get_current_user_from_header())
):
    education = await CtrEducation(current_user).ctr_education()
    return ResponseData[EducationLevelInfoResponse](**education)
