from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.user.profile.other.training_in_scb.controller import (
    CtrTrainingInSCB
)
from app.api.v1.endpoints.user.profile.other.training_in_scb.schema import (
    TrainingInSCBResponse
)

router = APIRouter()


@router.get(
    path="/",
    name="[THÔNG TIN KHÁC] - C. ĐÀO TẠO TRONG NH",
    description="[THÔNG TIN KHÁC] - C. ĐÀO TẠO TRONG NH",
    responses=swagger_response(
        response_model=ResponseData[List[TrainingInSCBResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_training_in_scb(
        current_user=Depends(get_current_user_from_header())
):
    training_in_scb_info = await CtrTrainingInSCB(current_user).ctr_training_in_scb()
    return ResponseData[List[TrainingInSCBResponse]](**training_in_scb_info)
