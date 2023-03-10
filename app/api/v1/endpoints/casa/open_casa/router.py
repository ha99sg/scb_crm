from fastapi import APIRouter

from app.api.v1.endpoints.casa.open_casa.co_owner import \
    view as view_create_co_owner
from app.api.v1.endpoints.casa.open_casa.open_casa import \
    view as views_open_casa_info

router_module = APIRouter()

# views của thông tin Casa -> Mở tài khoản thanh toán

router_module.include_router(router=views_open_casa_info.router)

# views của thông tin Casa -> Đồng sở hữu tài khoản

router_module.include_router(router=view_create_co_owner.router)
