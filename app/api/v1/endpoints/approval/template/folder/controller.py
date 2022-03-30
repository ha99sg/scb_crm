from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.template.folder.repository import (
    repos_get_approval_template_folder_info
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer


class CtrTemplateFolder(BaseController):
    async def ctr_get_approval_template_folder_info(self, cif_id: str):
        # check cif đang tạo
        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        approval_form_info = self.call_repos(await repos_get_approval_template_folder_info(cif_id=cif_id))
        return self.response(data=approval_form_info)