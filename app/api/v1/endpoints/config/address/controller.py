from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.address import (
    AddressCountry, AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue


class CtrAddress(BaseController):
    async def ctr_province_info(self, country_id: str):
        provinces_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressProvince,
                country_id=country_id,
            )
        )
        return self.response(provinces_info)

    async def ctr_district_info(self, province_id: str):
        districts_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressDistrict,
                province_id=province_id
            )
        )
        return self.response(districts_info)

    async def ctr_ward_info(self, district_id: str):
        wards_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressWard,
                district_id=district_id
            )
        )
        return self.response(wards_info)

    async def ctr_place_of_issue(self, country_id: str):
        place_of_issues_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=PlaceOfIssue,
                country_id=country_id
            )
        )
        return self.response(place_of_issues_info)

    async def ctr_country_info(self):
        country_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session,
                model=AddressCountry
            )
        )
        return self.response(country_info)
