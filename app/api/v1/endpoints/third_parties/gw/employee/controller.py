from app.api.base.controller import BaseController
from app.api.v1.endpoints.third_parties.gw.employee.repository import (
    repos_gw_get_employee_info_from_code,
    repos_gw_get_employee_info_from_user_name,
    repos_gw_get_employee_list_from_org_id,
    repos_gw_get_retrieve_employee_info_from_code,
    repos_gw_get_retrieve_reward_info_from_code,
    repos_gw_get_retrieve_working_process_info_from_code
)
from app.third_parties.oracle.models.master_data.customer import CustomerGender
from app.utils.constant.cif import CRM_GENDER_TYPE_FEMALE, CRM_GENDER_TYPE_MALE
from app.utils.constant.gw import (
    GW_DATE_FORMAT, GW_DATETIME_FORMAT, GW_GENDER_FEMALE, GW_GENDER_MALE
)
from app.utils.functions import (
    date_string_to_other_date_string_format, dropdown_name
)


class CtrGWEmployee(BaseController):
    async def ctr_gw_get_employee_info_from_code(
            self,
            employee_code: str
    ):
        current_user = self.current_user
        gw_employee_info = self.call_repos(await repos_gw_get_employee_info_from_code(
            employee_code=employee_code,
            current_user=current_user
        ))

        employee_info = gw_employee_info["selectEmployeeInfoFromCode_out"]["data_output"]["employee_info"]

        return self.response(data=dict(
            staff_code=employee_info['staff_code'],
            staff_name=employee_info['staff_name'],
            fullname_vn=employee_info['full_name'],
            work_location=employee_info['work_location'],
            email=employee_info['email_scb'],
            contact_mobile=employee_info['contact_mobile'],
            internal_mobile=employee_info['internal_mobile'],
            title_code=employee_info['title_code'],
            title_name=employee_info['title_name'],
            branch_org=employee_info['branch_org'],
            avatar=employee_info['avatar'],
        ))

    async def ctr_gw_get_employee_info_from_user_name(
            self,
            employee_name: str
    ):
        current_user = self.current_user
        gw_employee_info = self.call_repos(await repos_gw_get_employee_info_from_user_name(
            employee_name=employee_name,
            current_user=current_user
        ))

        employee_info = gw_employee_info["selectEmployeeInfoFromUserName_out"]["data_output"]["employee_info"]

        return self.response(data=dict(
            staff_code=employee_info['staff_code'],
            staff_name=employee_info['staff_name'],
            fullname_vn=employee_info['full_name'],
            work_location=employee_info['work_location'],
            email=employee_info['email_scb'],
            contact_mobile=employee_info['contact_mobile'],
            internal_mobile=employee_info['internal_mobile'],
            title_code=employee_info['title_code'],
            title_name=employee_info['title_name'],
            branch_org=employee_info['branch_org'],
            avatar=employee_info['avatar'],
        ))

    async def ctr_gw_get_employee_list_from_org_id(
            self,
            org_id: str
    ):
        current_user = self.current_user
        gw_employee_infos = self.call_repos(await repos_gw_get_employee_list_from_org_id(
            org_id=org_id,
            current_user=current_user
        ))

        employee_infos = gw_employee_infos["selectEmployeeListFromOrgId_out"]["data_output"]["employee_info"]

        return self.response(data=dict(
            employee_infos=[dict(
                staff_code=employee_info['staff_code'],
                staff_name=employee_info['staff_name'],
                fullname_vn=employee_info['full_name'],
                work_location=employee_info['work_location'],
                email=employee_info['email_scb'],
                contact_mobile=employee_info['contact_mobile'],
                internal_mobile=employee_info['internal_mobile'],
                title_code=employee_info['title_code'],
                title_name=employee_info['title_name'],
                branch_org=employee_info['branch_org'],
                avatar=employee_info['avatar'],
            ) for employee_info in employee_infos],
            total_items=len(employee_infos)
        ))

    async def ctr_gw_get_retrieve_employee_info_from_code(
            self,
            staff_code: str, staff_type: str, department_code: str, org_id: str
    ):
        current_user = self.current_user
        gw_employee_info = self.call_repos(await repos_gw_get_retrieve_employee_info_from_code(
            staff_code=staff_code,
            staff_type=staff_type,
            department_code=department_code,
            org_id=org_id,
            current_user=current_user
        ))

        employee_info = gw_employee_info["retrieveEmployeeInfoFromCode_out"]["data_output"]["employee_info"]

        department_info = employee_info['department_info']

        identity_info = employee_info['id_info']
        address_info = employee_info['address_info']
        education_info = employee_info['education_info']
        language_info = employee_info['language_info_item']

        certificate_info_list = employee_info['certificate_info_list']
        profile_info = employee_info['profile_info']
        contract_info = employee_info['contract_info']

        date_of_birth = date_string_to_other_date_string_format(
            date_input=employee_info['birth_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        gender_code_or_name = employee_info["sex"]
        if gender_code_or_name == GW_GENDER_MALE:
            gender_code_or_name = CRM_GENDER_TYPE_MALE
        if gender_code_or_name == GW_GENDER_FEMALE:
            gender_code_or_name = CRM_GENDER_TYPE_FEMALE

        dropdown_gender = self.dropdown_mapping_crm_model_or_dropdown_name(
            model=CustomerGender, name=gender_code_or_name, code=gender_code_or_name
        )

        identity_issued_date = date_string_to_other_date_string_format(
            date_input=identity_info['id_issued_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        identity_expired_date = date_string_to_other_date_string_format(
            date_input=identity_info['id_expired_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        profile_join_date = date_string_to_other_date_string_format(
            date_input=profile_info['join_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        profile_probation_date = date_string_to_other_date_string_format(
            date_input=profile_info['probation_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        profile_official_date = date_string_to_other_date_string_format(
            date_input=profile_info['official_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        profile_seniority_date = date_string_to_other_date_string_format(
            date_input=profile_info['seniority_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        contract_effected_date = date_string_to_other_date_string_format(
            date_input=contract_info['contract_effected_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        contract_expired_date = date_string_to_other_date_string_format(
            date_input=contract_info['contract_expired_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        schedule_of_contract_effected_date = date_string_to_other_date_string_format(
            date_input=contract_info['schedule_of_contract_effected_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        schedule_of_contract_expired_date = date_string_to_other_date_string_format(
            date_input=contract_info['schedule_of_contract_expired_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        stop_job_date = date_string_to_other_date_string_format(
            date_input=contract_info['stop_job_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        dropdown_department_info = dropdown_name(name=profile_info['department_info']['department_name'])
        dropdown_org_department_info = dropdown_name(name=profile_info['org_department_info']['department_name'])
        dropdown_temp_department_info = dropdown_name(name=profile_info['temp_department_info']['department_name'])

        english_issue_date = date_string_to_other_date_string_format(
            date_input=language_info['english_issue_date'],
            from_format=GW_DATETIME_FORMAT,
            to_format=GW_DATE_FORMAT
        )

        return self.response(data=dict(
            employee_info=dict(
                staff_code=employee_info['staff_code'],
                staff_name=employee_info['staff_name'],
                fullname_vn=employee_info['full_name'],
                email=employee_info['email_scb'],
                contact_mobile=employee_info['contact_mobile'],
                internal_mobile=employee_info['internal_mobile'],
                title_code=employee_info['title_code'],
                title_name=employee_info['title_name'],
                avatar=employee_info['avatar'],
                direct_management=employee_info['direct_management'],
                date_of_birth=date_of_birth,
                place_of_birth=employee_info['birth_province'],
                gender=dropdown_gender,
                ethnic=employee_info['nation'],
                religion=employee_info['religion'],
                nationality=employee_info['nationality'],
                marital_status=employee_info['marital_status']),
            department_info=dict(
                id=department_info['department_code'],
                code=department_info['department_code'],
                name=department_info['department_name']
            ),
            identity_info=dict(
                number=identity_info['id_num'],
                issued_date=identity_issued_date,
                expired_date=identity_expired_date,
                place_of_issue=identity_info['id_issued_location'],
            ),
            address_info=dict(
                original_address_line=address_info['original_address_line']
            ),
            education_info=dict(
                academy=education_info["academy"],
                education_level=education_info["education_level"],
                education_skill=education_info["education_skill"],
                major=education_info["major"],
                school_name=education_info["school_name"],
                training_form=education_info["training_form"],
                degree=education_info["degree"],
                gpa=education_info["gpa"]
            ),
            language_info=dict(
                english=language_info["english"],
                english_level=language_info["english_level"],
                english_mark=language_info["english_mark"],
                english_issue_date=english_issue_date
            ),
            certificate_infos=[dict(
                it_certificate=certificate_info["it_certificate"],
                it_certificate_level=certificate_info["it_certificate_level"],
                it_certificate_mark=certificate_info["it_certificate_mark"]
            ) for certificate_info in certificate_info_list["certificate_info_item"]],
            profile_info=dict(
                join_date=profile_join_date,
                probation_date=profile_probation_date,
                official_date=profile_official_date,
                jobtitle_name=profile_info['jobtitle_name'],
                temp_jobtitle_name=profile_info['temp_jobtitle_name'],
                seniority_date=profile_seniority_date,

                resident_status=profile_info['resident_status'],
                department_info=dropdown_department_info,
                org_department_info=dropdown_org_department_info,
                temp_department_info=dropdown_temp_department_info,
            ),
            contract_info=dict(
                contract_type=contract_info['contract_type'],
                contract_name=contract_info['contract_name'],
                contract_effected_date=contract_effected_date,
                contract_expired_date=contract_expired_date,
                schedule_of_contract_num=contract_info['schedule_of_contract_num'],
                schedule_of_contract_effected_date=schedule_of_contract_effected_date,
                schedule_of_contract_expired_date=schedule_of_contract_expired_date,
                stop_job_date=stop_job_date
            )
        ))

    async def ctr_gw_get_retrieve_working_process_info_from_code(self, staff_code: str):
        current_user = self.current_user
        gw_working_process_info = self.call_repos(await repos_gw_get_retrieve_working_process_info_from_code(
            staff_code=staff_code,
            current_user=current_user
        ))

        working_process_infos = gw_working_process_info['selectWorkingProcessInfoFromCode_out']['data_output'][
            'working_process_info_list']['working_process_info_item']

        return self.response(data=dict(
            total_items=len(working_process_infos),
            working_process_infos=[
                dict(company=working_process_info['company'],
                     from_date=date_string_to_other_date_string_format(
                         date_input=working_process_info['from_date'],
                         from_format=GW_DATETIME_FORMAT,
                         to_format=GW_DATE_FORMAT),
                     to_date=date_string_to_other_date_string_format(
                         date_input=working_process_info['to_date'],
                         from_format=GW_DATETIME_FORMAT,
                         to_format=GW_DATE_FORMAT),
                     position=working_process_info['position'], )
                for working_process_info in working_process_infos]))

    async def ctr_gw_get_retrieve_reward_info_from_code(self, staff_code: str):
        current_user = self.current_user
        gw_reward_info = self.call_repos(await repos_gw_get_retrieve_reward_info_from_code(
            staff_code=staff_code,
            current_user=current_user
        ))

        reward_infos = gw_reward_info['selectRewardInfoFromCode_out']['data_output'][
            'reward_info_list']['reward_info_item']

        return self.response(data=dict(
            total_items=len(reward_infos),
            working_process_infos=[
                dict(effect_date=date_string_to_other_date_string_format(
                    date_input=reward_info['reward_effect_date'],
                    from_format=GW_DATETIME_FORMAT,
                    to_format=GW_DATE_FORMAT
                ),
                    reward_num=reward_info['reward_num'],
                    title=reward_info['reward_title'],
                    level=reward_info['reward_level'],
                    jobtitle=reward_info['reward_jobtitle'],
                    department=reward_info['reward_department'],
                    reason=reward_info['reward_reason'],
                    form=reward_info['reward_form'],
                    of_amount=reward_info['reward_of_amount'],
                    signing_date=date_string_to_other_date_string_format(
                        date_input=reward_info['reward_signing_date'],
                        from_format=GW_DATETIME_FORMAT,
                        to_format=GW_DATE_FORMAT),
                    signer=reward_info['reward_signer'])
                for reward_info in reward_infos]))
