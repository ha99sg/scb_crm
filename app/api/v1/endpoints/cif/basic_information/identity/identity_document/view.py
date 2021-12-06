from typing import List, Union

from fastapi import APIRouter, Body, Depends, File, Form, Path, UploadFile
from starlette import status
from starlette.requests import Request

from app.api.base.schema import ResponseData
from app.api.base.swagger import swagger_response
from app.api.v1.dependencies.authenticate import get_current_user_from_header
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.controller import (
    CtrIdentityDocument
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.ocr_schema_response import (
    OCRFrontSideIdentityCardResponse, OCRPassportResponse
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_request import (
    CitizenCardSaveRequest, IdentityCardSaveRequest, PassportSaveRequest
)
from app.api.v1.endpoints.cif.basic_information.identity.identity_document.schema_response import (
    CitizenCardDetailResponse, IdentityCardDetailResponse, LogResponse,
    PassportDetailResponse
)
from app.api.v1.schemas.utils import SaveSuccessResponse
from app.utils.constant.cif import (
    EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD,
    IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD, IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD
)

router = APIRouter()


@router.get(
    path="/",
    name="1. GTĐD - A. GTĐD - Chi tiết",
    description="Chi tiết",
    responses=swagger_response(
        response_model=Union[
            ResponseData[IdentityCardDetailResponse],
            ResponseData[CitizenCardDetailResponse],
            ResponseData[PassportDetailResponse]
        ],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_detail(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_identity_document = CtrIdentityDocument(current_user)

    identity_document_type_id, detail_info = await ctr_identity_document.detail_identity(cif_id=cif_id)

    if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_IDENTITY_CARD:
        return ResponseData[IdentityCardDetailResponse](**detail_info)
    if identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
        return ResponseData[CitizenCardDetailResponse](**detail_info)
    else:
        return ResponseData[PassportDetailResponse](**detail_info)


@router.get(
    path="/log/",
    name="1. GTĐD - A. GTĐD - Lịch sử",
    description="Lịch sử",
    responses=swagger_response(
        response_model=ResponseData[List[LogResponse]],
        success_status_code=status.HTTP_200_OK
    )
)
async def view_list_logs(
        cif_id: str = Path(..., description='Id CIF ảo'),
        current_user=Depends(get_current_user_from_header())
):
    ctr_identity_document = CtrIdentityDocument(current_user)

    logs_info = await ctr_identity_document.get_list_log(
        cif_id=cif_id
    )

    return ResponseData[List[LogResponse]](
        **logs_info
    )

########################################################################################################################

router_special = APIRouter()


@router_special.post(
    path="/basic-information/identity/identity-document/",
    name="1. GTĐD - A. GTĐD - Lưu",
    description="Lưu",
    responses=swagger_response(
        response_model=ResponseData[SaveSuccessResponse],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_save(
        request: Request,
        identity_document_request: Union[IdentityCardSaveRequest, CitizenCardSaveRequest, PassportSaveRequest] = Body(
            ...
        ),
        current_user=Depends(get_current_user_from_header())
):
    # Vì 2 Model CMND, CCCD có cùng dạng ở level 1 nên phải kiểm tra để parse data sang model chuẩn tránh việc nhầm lẫn
    if isinstance(identity_document_request, IdentityCardSaveRequest):
        request_body = await request.json()
        request_body_identity_document_type_id = request_body['identity_document_type']['id']
        if request_body_identity_document_type_id == IDENTITY_DOCUMENT_TYPE_CITIZEN_CARD:
            identity_document_request = CitizenCardSaveRequest(**request_body)

    save_info = await CtrIdentityDocument(current_user).save_identity(identity_document_request)
    return ResponseData[SaveSuccessResponse](**save_info)


@router_special.post(
    path="/basic-information/identity/identity-document/ocr/",
    name="1. GTĐD - A. GTĐD - Upload & OCR",
    description="Upload ảnh giấy tờ tùy thân + Lấy thông tin OCR của giấy tờ tùy thân",
    responses=swagger_response(
        response_model=Union[
            ResponseData[OCRFrontSideIdentityCardResponse],
            ResponseData[OCRPassportResponse]
        ],
        success_status_code=status.HTTP_200_OK
    ),
    tags=['[CIF] I. TTCN']
)
async def view_upload_identity_document_image(
        identity_type: int = Form(..., description="""Loại giấy tờ định danh
            \n`0` : Hộ chiếu
            \n`1` : CMND mặt trước
            \n`2` : CMND mặt sau
            \n`3` : CCCD mặt trước
            \n`4` : CCCD mặt sau
        """),
        image_file: UploadFile = File(..., description='File hình ảnh giấy tờ định danh'),
        current_user=Depends(get_current_user_from_header())
):
    upload_info = await CtrIdentityDocument(current_user).upload_identity_document_and_ocr(
        image_file=image_file,
        identity_type=identity_type
    )

    # TODO: các loại khác
    if identity_type == EKYC_IDENTITY_TYPE_FRONT_SIDE_IDENTITY_CARD:
        return ResponseData[OCRFrontSideIdentityCardResponse](**upload_info)
    else:
        return ResponseData[OCRPassportResponse](**upload_info)
