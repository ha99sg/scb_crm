from fastapi import APIRouter

from app.api.v1.endpoints.user import view as views_user
from app.api.v1.endpoints.user.contact import view as router_contact
from app.api.v1.endpoints.user.profile import router as router_profile

router_module = APIRouter()

# Thông tin Nhân viên
router_module.include_router(router=router_profile.router_module, prefix="/profiles", tags=["User Profile"])

# router của thông tin user
router_module.include_router(router=views_user.router, tags=["User"])

# customer contact
router_module.include_router(router=router_contact.router, prefix="", tags=["User Contact"])
