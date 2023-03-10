from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.level.foreign.controller import (
    CtrForeign
)
from app.api.v1.endpoints.user.profile.level.foreign.schema import (
    ForeignLanguageLevelInfoResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN TRÌNH ĐỘ] - B. TRÌNH ĐỘ NGOẠI NGỮ",
    description="[THÔNG TIN TRÌNH ĐỘ] - B. TRÌNH ĐỘ NGOẠI NGỮ",
    responses=swagger_response(
        response_model=ResponseData[List[ForeignLanguageLevelInfoResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_foreign(
        current_user=Depends(get_current_user_from_header())
):
    foreign = await CtrForeign(current_user).ctr_foreign()
    return ResponseData[List[ForeignLanguageLevelInfoResponse]](**foreign)
