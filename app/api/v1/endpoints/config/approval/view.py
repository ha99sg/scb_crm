from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.config.approval.controller import CtrConfigApproval
from app.api.v1.schemas.utils import DropdownResponse
from app.utils.constant.approval import ROLE_CODES
from app.utils.constant.business_type import BUSINESS_TYPES
from app.utils.functions import make_description_from_dict

router = APIRouter()


@router.get(
    path="/action/",
    name="Stage Action",
    description="Hành động",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_stage_action_info(
    business_type_code: str = Query(..., description="Mã Nghiệp vụ" + make_description_from_dict(BUSINESS_TYPES)),
    role_code: str = Query(..., description="Mã Quyền thực hiện" + make_description_from_dict(ROLE_CODES)),
    current_user=Depends(get_current_user_from_header())
):
    stage_action_info = await CtrConfigApproval(current_user=current_user).ctr_stage_action(
        business_type_code=business_type_code,
        role_code=role_code
    )
    return ResponseData[List[DropdownResponse]](**stage_action_info)


@router.get(
    path="/status/",
    name="Stage Status",
    description="Trạng thái phê duyệt",
    responses=swagger_response(
        response_model=ResponseData[List[DropdownResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_stage_status_info(
    current_user=Depends(get_current_user_from_header())
):
    stage_status_info = await CtrConfigApproval(current_user=current_user).ctr_stage_status()
    return ResponseData[List[DropdownResponse]](**stage_status_info)
