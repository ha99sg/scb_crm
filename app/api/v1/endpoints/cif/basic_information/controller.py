from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.basic_information.repository import (
    repos_detail_relationship
)


class CtrBasicInformation(BaseController):
    async def detail_relationship(self, cif_id: str):
        basic_information_data = self.call_repos(await repos_detail_relationship(cif_id=cif_id))
        return self.response(data=basic_information_data)
