from typing import List

from app.api.base.controller import BaseController
from app.api.v1.endpoints.blacklist.repository import (
    repo_add_blacklist, repo_view_blacklist, repos_get_total_indentity_id
)
from app.api.v1.endpoints.blacklist.schema import BlacklistRequest


class CtrBlackList(BaseController):
    async def ctr_create_blacklist(self, data_blacklist: BlacklistRequest):
        data_insert = {
            'full_name': data_blacklist.full_name,
            'date_of_birth': data_blacklist.date_of_birth,
            'identity_id': data_blacklist.identity_id,
            'issued_date': data_blacklist.issued_date,
            'place_of_issue_id': data_blacklist.place_of_issue_id,
            'cif_num': data_blacklist.cif_num,
            'casa_account_num': data_blacklist.casa_account_num,
            'branch_id': data_blacklist.branch_id,
            'date_open_account_number': data_blacklist.date_open_account_number,
            'mobile_num': data_blacklist.mobile_num,
            'place_of_residence': data_blacklist.place_of_residence,
            'place_of_origin': data_blacklist.place_of_origin,
            'reason': data_blacklist.reason,
            'job_content': data_blacklist.job_content,
            'blacklist_source': data_blacklist.blacklist_source,
            'document_no': data_blacklist.document_no,
            'blacklist_area': data_blacklist.blacklist_area,
            'created_at': data_blacklist.created_at,
            'updated_at': data_blacklist.updated_at,
        }

        self.call_repos(await repo_add_blacklist(
            data_blacklist=data_insert,
            session=self.oracle_session
        ))
        return self.response(data={
            **data_insert
        })

    async def ctr_view_blacklist(self,
                                 identity_id: List[str],
                                 # cif_num:str,
                                 # casa_account_num:str
                                 ):

        limit = self.pagination_params.limit
        current_page = 1
        if self.pagination_params.page:
            current_page = self.pagination_params.page

        blacklist = self.call_repos(await repo_view_blacklist(
            session=self.oracle_session,
            limit=limit,
            page=current_page,
            identity_id=identity_id
        ))

        total_item = self.call_repos(
            await repos_get_total_indentity_id(
                session=self.oracle_session,
                identity_id=identity_id
            )
        )

        total_page = 0
        if total_item != 0:
            total_page = total_item / limit

        if total_item % limit != 0:
            total_page += 1

        data = [{
            'id': item_blacklist.Blacklist.id,
            'full_name': item_blacklist.Blacklist.full_name,
            'date_of_birth': item_blacklist.Blacklist.date_of_birth,
            'identity_id': item_blacklist.Blacklist.identity_id,
            'issued_date': item_blacklist.Blacklist.issued_date,
            'place_of_issue_id': item_blacklist.Blacklist.place_of_issue_id,
            'cif_num': item_blacklist.Blacklist.cif_num,
            'casa_account_num': item_blacklist.Blacklist.casa_account_num,
            'branch_id': item_blacklist.Blacklist.branch_id,
            'date_open_account_number': item_blacklist.Blacklist.date_open_account_number,
            'mobile_num': item_blacklist.Blacklist.mobile_num,
            'place_of_residence': item_blacklist.Blacklist.place_of_residence,
            'place_of_origin': item_blacklist.Blacklist.place_of_origin,
            'reason': item_blacklist.Blacklist.reason,
            'job_content': item_blacklist.Blacklist.job_content,
            'blacklist_source': item_blacklist.Blacklist.blacklist_source,
            'document_no': item_blacklist.Blacklist.document_no,
            'blacklist_area': item_blacklist.Blacklist.blacklist_area,
            'created_at': item_blacklist.Blacklist.created_at,
            'updated_at': item_blacklist.Blacklist.updated_at,
        } for item_blacklist in blacklist]

        return self.response_paging(
            data=data,
            current_page=current_page,
            total_items=total_item,
            total_page=total_page
        )
