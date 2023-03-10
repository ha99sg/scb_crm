from fastapi import APIRouter

from app.api.v1.endpoints.approval_v2 import view as views_approval_info
from app.api.v1.endpoints.approval_v2.face import view as views_face_info
from app.api.v1.endpoints.approval_v2.fingerprint import \
    view as views_fingerprint_info
from app.api.v1.endpoints.approval_v2.signature import \
    view as views_signature_info
from app.api.v1.endpoints.approval_v2.template import view as views_template

router_module = APIRouter()

# router của thông tin phê duyệt
router_module.include_router(router=views_approval_info.router)

# router của [Thông tin xác thực] -> Khuôn mặt
router_module.include_router(router=views_face_info.router)

# router của [Thông tin xác thực] -> Chữ ký
router_module.include_router(router=views_signature_info.router)

# router của [Thông tin xác thực] -> Vân tay
router_module.include_router(router=views_fingerprint_info.router)

# router api cho TMS
router_module.include_router(router=views_template.router, prefix="/template")
