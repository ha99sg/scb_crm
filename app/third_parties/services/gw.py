import json
from datetime import date
from typing import Optional

import aiohttp
from loguru import logger
from starlette import status

from app.api.v1.endpoints.user.schema import UserInfoResponse
from app.settings.service import SERVICE
from app.utils.constant.gw import (
    GW_AUTHORIZED_REF_DATA_MGM_ACC_NUM, GW_CO_OWNER_REF_DATA_MGM_ACC_NUM,
    GW_CURRENT_ACCOUNT_CASA, GW_CURRENT_ACCOUNT_FROM_CIF,
    GW_CUSTOMER_REF_DATA_MGMT_CIF_NUM, GW_DEPOSIT_ACCOUNT_FROM_CIF,
    GW_DEPOSIT_ACCOUNT_TD, GW_EMPLOYEE_FROM_CODE, GW_EMPLOYEE_FROM_NAME,
    GW_EMPLOYEES, GW_ENDPOINT_URL_CHECK_EXITS_ACCOUNT_CASA,
    GW_ENDPOINT_URL_DEPOSIT_OPEN_ACCOUNT_TD,
    GW_ENDPOINT_URL_HISTORY_CHANGE_FIELD, GW_ENDPOINT_URL_INTERBANK_TRANSFER,
    GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_ACCOUNT_NUMBER,
    GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_CARD_NUMBER,
    GW_ENDPOINT_URL_INTERNAL_TRANSFER, GW_ENDPOINT_URL_PAY_IN_CASH,
    GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_ACCOUNT_NUMBER,
    GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_CARD_NUMBER,
    GW_ENDPOINT_URL_PAYMENT_AMOUNT_BLOCK,
    GW_ENDPOINT_URL_PAYMENT_AMOUNT_UNBLOCK, GW_ENDPOINT_URL_REDEEM_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_AUTHORIZED_ACCOUNT_NUM,
    GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_ACCOUNT_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_CARD_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_CHANGE_STATUS_ACCOUNT_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_CLOSE_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_CO_OWNER_ACCOUNT_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA,
    GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM,
    GW_ENDPOINT_URL_RETRIEVE_CUS_OPEN_CIF,
    GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF,
    GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD,
    GW_ENDPOINT_URL_RETRIEVE_DISCIPLINE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_EBANK_BY_CIF_NUMBER,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME,
    GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_LIST_FROM_ORG_ID,
    GW_ENDPOINT_URL_RETRIEVE_KPIS_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_OPEN_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_TD_ACCOUNT,
    GW_ENDPOINT_URL_RETRIEVE_REWARD_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_STAFF_OTHER_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_TELE_TRANSFER_INFO,
    GW_ENDPOINT_URL_RETRIEVE_TOPIC_INFO_FROM_CODE,
    GW_ENDPOINT_URL_RETRIEVE_WORKING_PROCESS_INFO_FROM_CODE,
    GW_ENDPOINT_URL_SELECT_BRANCH_BY_BRANCH_ID,
    GW_ENDPOINT_URL_SELECT_BRANCH_BY_REGION_ID,
    GW_ENDPOINT_URL_SELECT_CATEGORY,
    GW_ENDPOINT_URL_SELECT_EMPLOYEE_INFO_FROM_CODE,
    GW_ENDPOINT_URL_SELECT_SERIAL_NUMBER,
    GW_ENDPOINT_URL_SELECT_STATISTIC_BANKING_BY_PERIOD,
    GW_ENDPOINT_URL_SELECT_USER_INFO, GW_ENDPOINT_URL_TELE_TRANSFER,
    GW_ENDPOINT_URL_TT_LIQUIDATION, GW_ENDPOINT_URL_WITHDRAW,
    GW_FUNCTION_OPEN_CASA, GW_HISTORY_ACCOUNT_NUM,
    GW_HISTORY_CHANGE_FIELD_ACCOUNT, GW_RESPONSE_STATUS_SUCCESS,
    GW_RETRIEVE_CASA_ACCOUNT_DETAIL, GW_SELF_SELECTED_ACCOUNT_FLAG,
    GW_SELF_UNSELECTED_ACCOUNT_FLAG
)
from app.utils.functions import date_to_string


class ServiceGW:
    session: Optional[aiohttp.ClientSession] = None

    url = SERVICE["gw"]['url']

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    async def call_api(self, api_url: str, request_data: json, output_key: str, service_name: str):
        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][{service_name}] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    if return_data[output_key]['transaction_info']['transaction_error_code'] \
                            != GW_RESPONSE_STATUS_SUCCESS:
                        return False, return_data
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # START --- CASA
    ####################################################################################################################

    async def get_casa_account_from_cif(self, current_user: UserInfoResponse, casa_cif_number: str):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_CURRENT_ACCOUNT_FROM_CIF,
                "transaction_value": {
                    "cif_num": casa_cif_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectCurrentAccountFromCIF_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA_FROM_CIF}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_casa_account(self, current_user: UserInfoResponse, account_number: str):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_CURRENT_ACCOUNT_CASA,
                "transaction_value": {
                    "account_num": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveCurrentAccountCASA_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CURRENT_ACCOUNT_CASA}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_report_history_casa_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str,
            from_date: date,
            to_date: date
    ):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number,
                    "P_FDATE": date_to_string(from_date),
                    "P_TDATE": date_to_string(to_date)
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportHisCaSaFromAcc_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_HIS_CASA_ACCOUNT}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_report_statement_casa_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str,
            from_date: date,
            to_date: date
    ):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number,
                    "P_FDATE": date_to_string(from_date),
                    "P_TDATE": date_to_string(to_date)
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportStatementCaSaFromAcc_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_CASA_ACCOUNT}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_report_casa_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str,
    ):
        """
        Lấy thông tin biểu đồ hình tròn
        """
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportCaSaFromAcc_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_CASA_ACCOUNT}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_open_casa_account(
            self,
            current_user: UserInfoResponse,
            cif_number,
            self_selected_account_flag: bool,
            casa_account_info
    ):
        """
        Mở tài khoản thanh toán
        """
        account_num = casa_account_info.casa_account_number if casa_account_info.casa_account_number else ''
        data_input = {
            "customer_info": {
                "cif_info": {
                    "cif_num": cif_number
                },
                "account_info": {
                    "acc_spl": GW_SELF_SELECTED_ACCOUNT_FLAG if self_selected_account_flag else GW_SELF_UNSELECTED_ACCOUNT_FLAG,
                    "account_num": account_num,
                    "account_currency": casa_account_info.currency_id,
                    "account_class_code": casa_account_info.acc_class_id,
                    "p_blk_cust_account": "",
                    "p_blk_provision_main": "",
                    "p_blk_provdetails": "",
                    "p_blk_report_gentime1": "",
                    "p_blk_accmaintinstr": "",
                    "p_blk_report_gentime2": "",
                    "p_blk_multi_account_generation": "",
                    "p_blk_account_generation": "",
                    "p_blk_interim_details": "",
                    "p_blk_accprdres": "",
                    "p_blk_acctxnres": "",
                    "p_blk_authbicdetails": "",
                    "p_blk_acstatuslines": "",
                    "p_blk_jointholders": "",
                    "p_blk_acccrdrlmts": "",
                    "p_blk_intdetails": "",
                    "p_blk_intprodmap": "",
                    "p_blk_inteffdtmap": "",
                    "p_blk_intsde": "",
                    "p_blk_tddetails": "",
                    "p_blk_amount_dates": "",
                    "p_blk_turnovers": "",
                    "p_blk_noticepref": "",
                    "p_blk_acc_nominees": "",
                    "p_blk_dcdmaster": "",
                    "p_blk_tdpayindetails": "",
                    "p_blk_tdpayoutdetails": "",
                    "p_blk_tod_renew": "",
                    "p_blk_od_limit": "",
                    "p_blk_doctype_checklist": "",
                    "p_blk_doctype_remarks": "",
                    "p_blk_sttms_od_coll_linkages": "",
                    "p_blk_cust_acc_check": "",
                    "p_blk_cust_acc_card": "",
                    "p_blk_intermediary": "",
                    "p_blk_summary": "",
                    "p_blk_accls_rollover": "",
                    "p_blk_promotions": "",
                    "p_blk_link_pricing": "",
                    "p_blk_linkedentities": "",
                    "p_blk_custacc_icccspcn": "",
                    "p_blk_custacc_icchspcn": "",
                    "p_blk_custacc_iccinstr": "",
                    "p_blk_custaccdet": "",
                    "p_blk_custacc_sicdiary": "",
                    "p_blk_custacc_stccusbl": "",
                    "p_blk_accclose": "",
                    "p_blk_acc_svcacsig": "",
                    "p_blk_sttms_debit": "",
                    "p_blk_tddetailsprn": "",
                    "p_blk_extsys_ws_master": "",
                    "p_blk_custacc_iccintpo": "",
                    "p_blk_sttms_cust_account": "",
                    "p_blk_customer_acc": "",
                    "p_blk_customer_accis": "",
                    "p_blk_master": "",
                    "p_blk_sttms_cust_acc_swp": "",
                    "p_blk_acc_chnl": ""
                },
                "staff_info_checker": {
                    "staff_name": "BINHNTH"  # TODO
                    # "staff_name": current_user.username
                },
                "staff_info_maker": {
                    "staff_name": "HIEUPN"  # TODO
                    # "staff_name": casa_account_info.maker_id
                },
                "udf_info": {
                    "udf_json_array": []
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=GW_FUNCTION_OPEN_CASA, data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_OPEN_CASA_ACCOUNT}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data, request_data
                else:
                    return_data = await response.json()
                    if return_data['openCASA_out']['transaction_info']['transaction_error_code'] \
                            != GW_RESPONSE_STATUS_SUCCESS:
                        return False, return_data, request_data

                    return True, return_data, request_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data, request_data

    async def get_close_casa_account(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        """
        Đóng tài khoản thanh toán
        """

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="closeCASA_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CLOSE_CASA_ACCOUNT}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data, request_data
                else:
                    return_data = await response.json()
                    return True, return_data, request_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data, request_data

    async def get_tele_transfer(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="teleTransfer_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_TELE_TRANSFER_INFO}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_ben_name_by_account_number(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveBenNameByAccNum_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_ACCOUNT_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_ben_name_by_card_number(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveBenNameByCardNum_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_BEN_NAME_BY_CARD_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def change_status_account(
            self,
            current_user: UserInfoResponse,
            data_input
    ):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="accountChangeStatus_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CHANGE_STATUS_ACCOUNT_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data, request_data
                else:
                    return_data = await response.json()
                    return True, return_data, request_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data, request_data

    ####################################################################################################################
    # END --- CASA
    ####################################################################################################################

    ####################################################################################################################
    # START --- DEPOSIT TD
    ####################################################################################################################
    async def get_report_statement_td_account(
            self,
            current_user: UserInfoResponse,
            account_number: str,
            transaction_name: str,
            from_date: date,
            to_date: date
    ):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_ACC": account_number,
                    "P_FDATE": date_to_string(from_date),
                    "P_TDATE": date_to_string(to_date)
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportStatementTDFromAcc_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REPORT_STATEMENT_TD_ACCOUNT}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Report] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def select_report_td_from_cif_data_input(
            self,
            current_user: UserInfoResponse,
            transaction_name: str,
            endpoint: str,
            cif_number: str
    ):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "P_CIF": cif_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectReportTDFromCif_in", data_input=data_input
        )

        api_url = f"{self.url}{endpoint}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_deposit_account_from_cif(self, current_user: UserInfoResponse, account_cif_number):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_DEPOSIT_ACCOUNT_FROM_CIF,
                "transaction_value": {
                    "cif_num": account_cif_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectDepositAccountFromCIF_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_FROM_CIF}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_deposit_account_td(self, current_user: UserInfoResponse, account_number):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_DEPOSIT_ACCOUNT_TD,
                "transaction_value": {
                    "account_num": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveDepositAccountTD_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_DEPOSIT_ACCOUNT_TD}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def deposit_open_account_td(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="openTD_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_DEPOSIT_OPEN_ACCOUNT_TD}"
        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data, request_data
                else:
                    return_data = await response.json()
                    return True, return_data, request_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data, request_data

    ####################################################################################################################
    # END --- DEPOSIT TD
    ####################################################################################################################
    ####################################################################################################################
    # START --- RETRIEVE EBANK
    ####################################################################################################################
    async def get_retrieve_ebank_td(self, current_user: UserInfoResponse, cif_num):
        data_input = {
            "cif_info": {
                "cif_num": cif_num
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveEbankStatusByCif_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EBANK_BY_CIF_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # END --- RETRIEVE EBANK
    ####################################################################################################################
    ####################################################################################################################
    # START --- CUSTOMER
    ####################################################################################################################

    async def get_customer_info_list(
            self,
            current_user: UserInfoResponse,
            cif_number: str,
            identity_number: str,
            mobile_number: str,
            full_name: str
    ):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_CUSTOMER_REF_DATA_MGMT_CIF_NUM,
                "transaction_value": {
                    "cif_num": cif_number,
                    "id_num": identity_number,
                    "mobile_num": mobile_number,
                    "full_name": full_name
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectCustomerRefDataMgmtCIFNum_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CUS_DATA_MGMT_CIF_NUM}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_customer_info_detail(self, current_user: UserInfoResponse, customer_cif_number):
        data_input = {
            "transaction_info": {
                "transaction_name": "CustFromCIF",
                "transaction_value": {
                    "cif_num": customer_cif_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveCustomerRefDataMgmt_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CUS_REF_DATA_MGMT}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_co_owner(self, current_user: UserInfoResponse, account_number):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_CO_OWNER_REF_DATA_MGM_ACC_NUM,
                "transaction_value": {
                    "account_num": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectCoownerRefDataMgmtAccNum_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CO_OWNER_ACCOUNT_NUM}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_authorized(self, current_user: UserInfoResponse, account_number):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_AUTHORIZED_REF_DATA_MGM_ACC_NUM,
                "transaction_value": {
                    "account_num": account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectAuthorizedRefDataMgmtAccNum_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_AUTHORIZED_ACCOUNT_NUM}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # END --- CUSTOMER
    ####################################################################################################################

    ####################################################################################################################
    # START --- EMPLOYEE
    ####################################################################################################################
    async def get_employee_info_from_code(self, current_user: UserInfoResponse, employee_code):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_EMPLOYEE_FROM_CODE,
                "transaction_value": {
                    "employee_code": employee_code
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectEmployeeInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_EMPLOYEE_INFO_FROM_CODE}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_employee_info_from_user_name(self, current_user: UserInfoResponse, employee_name):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_EMPLOYEE_FROM_NAME,
                "transaction_value": {
                    "employee_name": employee_name
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectEmployeeInfoFromUserName_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_USER_NAME}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_employee_list_from_org_id(self, current_user: UserInfoResponse, org_id):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_EMPLOYEES,
                "transaction_value": {
                    "org_id": org_id
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectEmployeeListFromOrgId_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_LIST_FROM_ORG_ID}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_retrieve_employee_info_from_code(self, current_user: UserInfoResponse, staff_code):
        data_input = {
            "employee_info": {
                "staff_code": staff_code,
                "staff_type": "CHI_TIET",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveEmployeeInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_EMPLOYEE_INFO_FROM_CODE}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_working_process_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectWorkingProcessInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_WORKING_PROCESS_INFO_FROM_CODE}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_reward_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code,
                "staff_type": "KHEN_THUONG",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectRewardInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_REWARD_INFO_FROM_CODE}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_discipline_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code,
                "staff_type": "KY_LUAT",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectDisciplineInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_DISCIPLINE_INFO_FROM_CODE}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_topic_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code,
                "staff_type": "DAO_TAO_NOI_BO",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectTopicInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_TOPIC_INFO_FROM_CODE}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_kpis_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": str(int(current_user.code))
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectKpisInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_KPIS_INFO_FROM_CODE}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def get_staff_other_info_from_code(self, current_user: UserInfoResponse):
        data_input = {
            "employee_info": {
                "staff_code": current_user.code,
                "staff_type": "OTHER_INFO",
                "department_info": {
                    "department_code": "ALL"
                },
                "branch_org": {
                    "org_id": "ALL"
                }
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectStaffOtherInfoFromCode_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_STAFF_OTHER_INFO_FROM_CODE}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def select_org_info(self, current_user: UserInfoResponse, transaction_name: str, endpoint: str,
                              function_name: str, id: str):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": {
                    "id": id
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name=function_name, data_input=data_input
        )

        api_url = f"{self.url}{endpoint}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # END --- EMPLOYEE
    ####################################################################################################################

    ####################################################################################################################
    # START --- CATEGORY
    ####################################################################################################################
    async def get_select_category(self, current_user: UserInfoResponse, transaction_name: str, transaction_value: str):
        data_input = {
            "transaction_info": {
                "transaction_name": transaction_name,
                "transaction_value": transaction_value
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectCategory_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_CATEGORY}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # END --- CATEGORY
    ####################################################################################################################
    # START --- HISTORY
    ####################################################################################################################
    async def get_history_change_field(self, current_user: UserInfoResponse):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_HISTORY_CHANGE_FIELD_ACCOUNT,
                "transaction_value": {
                    "account_num": GW_HISTORY_ACCOUNT_NUM
                }
            }
        }

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="historyChangeFieldAccount_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_HISTORY_CHANGE_FIELD}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # END --- HISTORY
    ####################################################################################################################
    # START --- CIF
    ####################################################################################################################
    async def open_cif(
            self,
            cif_id: str,
            customer_info: dict,
            account_info: dict,
            current_user
    ):
        data_input = {
            "customer_info": customer_info,
            "account_info": account_info
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="openCIFAuthorise_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_RETRIEVE_CUS_OPEN_CIF}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except Exception as ex:
            logger.error(str(ex))
            return False, {'message': str(ex)}

    ####################################################################################################################
    # END --- CIF
    ####################################################################################################################

    ####################################################################################################################
    # START --- UTILS
    ####################################################################################################################
    @staticmethod
    def gw_create_request_body(current_user: UserInfoResponse, data_input: dict,
                               function_name: str):
        return {
            function_name: {
                "transaction_info": {
                    "client_code": "CRM",
                    "client_ref_num": "20190702091907_4232781",
                    "client_ip": "10.4.4.x",
                    "server_ref_num": "string",
                    "branch_info": {
                        "branch_name": current_user.hrm_branch_name,
                        "branch_code": current_user.hrm_branch_code
                    }
                },
                "data_input": data_input
            }
        }

    ####################################################################################################################
    # END --- UTILS
    ####################################################################################################################
    # START --- CHECK_EXIST_CASA_ACCOUNT_NUMBER
    ####################################################################################################################
    async def check_exist_casa_account_number(self, current_user: UserInfoResponse, casa_account_number):
        data_input = {
            "transaction_info": {
                "transaction_name": GW_RETRIEVE_CASA_ACCOUNT_DETAIL,
                "transaction_value": {
                    "account_num": casa_account_number
                }
            }
        }
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveCurrentAccountCASA_in", data_input=data_input
        )

        api_url = f"{self.url}{GW_ENDPOINT_URL_CHECK_EXITS_ACCOUNT_CASA}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # END --- CHECK_EXIST_CASA_ACCOUNT_NUMBER
    ####################################################################################################################
    ####################################################################################################################
    # start --- withdraw
    ####################################################################################################################
    async def gw_withdraw(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="cashWithdrawals_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_WITHDRAW}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data, request_data
                else:
                    return_data = await response.json()
                    return True, return_data, request_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data, request_data

    ####################################################################################################################
    # end --- withdraw
    ####################################################################################################################

    ####################################################################################################################
    # start --- payment
    ####################################################################################################################

    async def gw_payment_amount_block(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="amountBlock_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAYMENT_AMOUNT_BLOCK}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data, request_data
                else:
                    return_data = await response.json()
                    return True, return_data, request_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data, request_data

    async def gw_payment_amount_unblock(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="amountUnBlock_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAYMENT_AMOUNT_UNBLOCK}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    if return_data != GW_RESPONSE_STATUS_SUCCESS:
                        return False, return_data
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def gw_interbank_transfer(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="interbankTransfer_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERBANK_TRANSFER}"

        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='interbankTransfer_out',
            service_name='interbankTransfer'
        )

        return response_data

    async def gw_payment_redeem_account(self, request_data):
        api_url = f"{self.url}{GW_ENDPOINT_URL_REDEEM_ACCOUNT}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def gw_pay_in_cash(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="payInCash_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAY_IN_CASH}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key='payInCash_out',
            service_name='payInCash'
        )

    async def gw_pay_in_cash_247_by_acc_num(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="payInCash247byAccNum_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_ACCOUNT_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def gw_payment_internal_transfer(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="internal_transfer_in", data_input=data_input)
        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERNAL_TRANSFER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def gw_tele_transfer(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="teleTransfer_in", data_input=data_input)

        api_url = f"{self.url}{GW_ENDPOINT_URL_TELE_TRANSFER}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key='teleTransfer_out',
            service_name='teleTransfer'
        )

    async def gw_payment_tt_liquidation(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="ttLiquidation_in", data_input=data_input)
        api_url = f"{self.url}{GW_ENDPOINT_URL_TT_LIQUIDATION}"

        return await self.call_api(
            api_url=api_url,
            request_data=request_data,
            output_key='ttLiquidation_out',
            service_name='ttLiquidation'
        )

    async def gw_payment_interbank_transfer(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="interbankTransfer_in", data_input=data_input)

        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERBANK_TRANSFER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def gw_payment_interbank_transfer_247_by_account_number(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="interbankTransfer247ByAccNum_in", data_input=data_input)

        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_ACCOUNT_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )
        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def gw_payment_interbank_transfer_247_by_card_number(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="interbankTransfer247ByCardNum_in", data_input=data_input)

        api_url = f"{self.url}{GW_ENDPOINT_URL_INTERBANK_TRANSFER_247_BY_CARD_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    async def gw_pay_in_cash_247_by_card_num(self, current_user: UserInfoResponse, data_input):

        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="payInCash247byCardNum_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_PAY_IN_CASH_247_BY_CARD_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Payment] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # start --- user
    ####################################################################################################################
    async def gw_detail_user(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectUserInfoByUserID_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_USER_INFO}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][UserInfo] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # START --- SERIAL
    ####################################################################################################################
    async def get_select_serial(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="retrieveSerialNumber_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_SERIAL_NUMBER}"

        return_errors = dict(
            loc="SERVICE GW",
            msg="",
            detail=""
        )
        return_data = dict(
            status=None,
            data=None,
            errors=return_errors
        )

        try:
            async with self.session.post(url=api_url, json=request_data) as response:
                logger.log("SERVICE", f"[GW][Serial] {response.status} {api_url}")
                if response.status != status.HTTP_200_OK:
                    if response.status < status.HTTP_500_INTERNAL_SERVER_ERROR:
                        return_error = await response.json()
                        return_data.update(
                            status=response.status,
                            errors=return_error['errors']
                        )
                    return False, return_data
                else:
                    return_data = await response.json()
                    return True, return_data
        except aiohttp.ClientConnectorError as ex:
            logger.error(str(ex))
            return False, return_data

    ####################################################################################################################
    # Branch Location
    ####################################################################################################################
    async def select_branch_by_region_id(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectBranchByRegionID_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_BRANCH_BY_REGION_ID}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='selectBranchByRegionID_out',
            service_name='selectBranchByRegionID'
        )
        return response_data

    async def select_branch_by_branch_id(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectBranchByBranchID_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_BRANCH_BY_BRANCH_ID}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='selectBranchByBranchID_out',
            service_name='selectBranchByBranchID'
        )
        return response_data

    ####################################################################################################################

    ####################################################################################################################
    # Statistic
    ####################################################################################################################
    async def select_statistic_banking_by_period(self, current_user: UserInfoResponse, data_input):
        request_data = self.gw_create_request_body(
            current_user=current_user, function_name="selectStatisticBankingByPeriod_in", data_input=data_input
        )
        api_url = f"{self.url}{GW_ENDPOINT_URL_SELECT_STATISTIC_BANKING_BY_PERIOD}"
        response_data = await self.call_api(
            request_data=request_data,
            api_url=api_url,
            output_key='selectStatisticBankingByPeriod_out',
            service_name='selectStatisticBankingByPeriod'
        )
        return response_data
    ####################################################################################################################
