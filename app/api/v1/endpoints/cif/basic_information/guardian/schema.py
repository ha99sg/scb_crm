from typing import List

from pydantic import Field

from app.api.base.schema import BaseSchema
from app.api.v1.schemas.cif import RelationshipResponse
from app.api.v1.schemas.utils import DropdownRequest


########################################################################################################################
# Response
########################################################################################################################
# Thông tin người giám hộ -> Danh sách người giám hộ
class GuardianResponse(RelationshipResponse):
    id: str = Field(..., description="ID người giám hộ")
    avatar_url: str = Field(..., description="URL avatar người giám hộ")


# Thông tin người giám hộ
class DetailGuardianResponse(BaseSchema):
    guardian_flag: bool = Field(..., description="Cờ có người giám hộ không")
    number_of_guardian: int = Field(..., description="Số người giám hộ")
    guardians: List[GuardianResponse] = Field(..., description="Danh sách người giám hộ")


########################################################################################################################
# Request Body
########################################################################################################################
# Thông tin người giám hộ
class SaveGuardianRequest(BaseSchema):
    cif_number: str = Field(..., description="Số CIF")
    customer_relationship: DropdownRequest = Field(..., description="Mối quan hệ với khách hàng")
