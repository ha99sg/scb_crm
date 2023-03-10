from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_balance_saving_account_data, repos_check_and_remove_exist_ebank,
    repos_check_and_remove_exist_sms_casa, repos_get_detail_reset_password,
    repos_get_detail_reset_password_teller, repos_get_e_banking,
    repos_get_payment_accounts, repos_get_sms_data,
    repos_get_sms_data_open_casa, repos_save_e_banking, repos_save_sms_casa
)
from app.api.v1.endpoints.cif.e_banking.schema import (
    EBankingRequest, EBankingSMSCasaRequest
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking, repos_get_customer, repos_get_initializing_customer
)
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.api.v1.endpoints.third_parties.gw.customer.repository import (
    repos_get_cif_number_open_cif
)
from app.api.v1.endpoints.third_parties.gw.ebank.repository import (
    repos_pull_e_banking_from_gw_cif_number_and_return_is_exist_ebank
)
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.master_data.customer import (
    CustomerRelationshipType
)
from app.utils.constant.cif import (
    BUSINESS_FORM_EB, PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING,
    PROFILE_HISTORY_STATUS_INIT
)
from app.utils.error_messages import ERROR_E_BANKING
from app.utils.functions import orjson_dumps


class CtrEBanking(BaseController):
    ####################################################################################################################
    # Đăng ký Ebanking
    ####################################################################################################################
    async def ctr_save_e_banking_and_sms(self, cif_id: str, e_banking_info: EBankingRequest = None,
                                         ebank_sms_casa_info: EBankingSMSCasaRequest = None,
                                         open_casa_flag: bool = False):

        current_user = self.current_user
        current_user_info = current_user.user_info

        self.call_repos(await repos_get_initializing_customer(cif_id=cif_id, session=self.oracle_session))

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))

        # Validate không có SĐT không cho tạo EB
        customer = self.call_repos(await repos_get_customer(
            cif_id=cif_id, session=self.oracle_session
        ))
        if not customer.mobile_number:
            return self.response_exception(
                msg=ERROR_E_BANKING,
                loc='ctr_save_e_banking_and_sms -> mobile_number',
                detail='customer mobile_number cannot null',
            )

        if e_banking_info:
            ebank_ibmb_username = e_banking_info.username
            ebank_ibmb_receive_password_code = e_banking_info.receive_password_code
            authentication_code_list = e_banking_info.authentication_code_list

            # dữ liệu để tạo ebanking trong DB
            data_insert = {
                "ebank_info": {
                    "customer_id": cif_id,
                    "account_name": ebank_ibmb_username,
                    "method_active_password_id": ebank_ibmb_receive_password_code,
                },
                "ebank_info_authen_list": [{
                    "method_authentication_id": authentication_code
                } for authentication_code in authentication_code_list]
            }

            self.call_repos(
                await repos_save_e_banking(
                    cif_id=cif_id,
                    data_insert=data_insert,
                    session=self.oracle_session
                ))
        # TH không đăng ký ebanking, xóa các thông tin cũ
        else:
            self.call_repos(await repos_check_and_remove_exist_ebank(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        if ebank_sms_casa_info:
            # Validate nếu truyền thiếu một số thông tin cần thiết:
            if not ebank_sms_casa_info.registry_balance_items:
                return self.response_exception(
                    msg=ERROR_E_BANKING,
                    loc='ctr_save_e_banking_and_sms -> ebank_sms_casa_info',
                    detail='registry_balance_items cannot empty',
                )

            # Kiểm tra mối quan hệ
            relationship_ids = []
            for registry_balance_item in ebank_sms_casa_info.registry_balance_items:
                for register_balance_casa in registry_balance_item.receiver_noti_relationship_items:
                    relationship_ids.append(register_balance_casa.relationship_type_id)
            await self.get_model_objects_by_ids(
                model=CustomerRelationshipType,
                model_ids=list(relationship_ids),
                loc="receiver_noti_relationship_items -> relationship_type_id"
            )

            # Dữ liệu để tạo sms_casa trong DB
            data_insert = {
                "reg_balance_options": ebank_sms_casa_info.reg_balance_options,
                "registry_balance_items": [{
                    "casa_id": registry_balance_item.casa_id,
                    "main_phone_number_info": registry_balance_item.main_phone_number_info,
                    "receiver_noti_relationship_items": registry_balance_item.receiver_noti_relationship_items,
                    "notify_code_list": registry_balance_item.notify_code_list
                } for registry_balance_item in ebank_sms_casa_info.registry_balance_items]
            }

            self.call_repos(
                await repos_save_sms_casa(
                    cif_id=cif_id,
                    data_insert=data_insert,
                    session=self.oracle_session,
                ))
        # TH không đăng ký sms, xóa các thông tin cũ
        else:
            self.call_repos(await repos_check_and_remove_exist_sms_casa(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_INIT_E_BANKING,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user_info
        )
        # Validate history data
        is_success, history_response = validate_history_data(history_datas)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        is_success, booking_response = await write_transaction_log_and_update_booking(
            log_data=orjson_dumps({
                "e_bank": e_banking_info.dict() if e_banking_info else "",
                "sms_casa": ebank_sms_casa_info.dict() if ebank_sms_casa_info else ""
            }),
            history_datas=orjson_dumps(history_datas),
            session=self.oracle_session,
            customer_id=cif_id,
            business_form_id=BUSINESS_FORM_EB
        )
        if not is_success:
            return self.response_exception(msg=booking_response['msg'])

        return self.response(data={
            "cif_id": cif_id,
            "booking": {
                "id": booking.id,
                "code": booking.code,
                "name": current_user.user_info.username
            }
        })

    ####################################################################################################################
    # End: Đăng ký Ebanking
    ####################################################################################################################
    async def ctr_get_e_banking(self, cif_id: str, open_casa_flag=False):

        current_user = self.current_user
        is_exist_ebank = False
        old_casa_account_for_selects, new_casa_account_for_selects = [], []
        if open_casa_flag:
            # Kiểm tra EN từ core
            cif_number = self.call_repos(await repos_get_cif_number_open_cif(
                cif_id=cif_id, session=self.oracle_session))

            is_exist_ebank = (await repos_pull_e_banking_from_gw_cif_number_and_return_is_exist_ebank(
                cif_id=cif_id,
                cif_number=cif_number,
                current_user=current_user,
                session=self.oracle_session
            )).data

            sms_casa, old_casa_account_for_selects, new_casa_account_for_selects = self.call_repos(await repos_get_sms_data_open_casa(
                cif_id=cif_id,
                cif_number=cif_number,
                current_user=self.current_user,
                session=self.oracle_session
            ))

        else:
            sms_casa = self.call_repos(await repos_get_sms_data(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        e_banking = self.call_repos(await repos_get_e_banking(
            cif_id=cif_id,
            session=self.oracle_session
        ))

        response = {
            "is_disable_ebank_flag": is_exist_ebank,
            "e_banking": e_banking if e_banking else None,
            "sms_casa": sms_casa if sms_casa else None,
            "sms_casa_select_info": {
                "old_casa_accounts": old_casa_account_for_selects,
                "new_casa_accounts": new_casa_account_for_selects,
            }
        }

        return self.response(data=response)

    async def ctr_balance_payment_account(self, cif_id: str):

        # Luồng tạo mới chỉ lấy tài khoản thanh toán trong DB
        # Lấy danh sách tài khoản thanh toán trong DB
        payment_accounts = self.call_repos(
            await repos_get_payment_accounts(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        payment_account_infos = []
        for casa_account, account_type in payment_accounts:
            payment_account_infos.append({
                "id": casa_account.id,
                "account_number": casa_account.casa_account_number,
                "product_name": account_type.name,
            })

        return self.response(data=payment_account_infos)

    async def get_detail_reset_password(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password(cif_id))

        return self.response(data=detail_reset_password_data)

    async def ctr_balance_saving_account(self, cif_id: str):
        balance_saving_account = self.call_repos(
            await repos_balance_saving_account_data(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        # response_data = []
        # if balance_saving_account:
        #     balance_saving_accounts = balance_saving_account['selectDepositAccountFromCIF_out']['accountInfo']
        #     for account in balance_saving_accounts:
        #         response_data.append({
        #             "id": account['customerInfo']['rowOrder'],
        #             "account_number": account['accountNum'],
        #             "name": account['customerInfo']['fullname'],
        #         })

        return self.response_paging(
            data=balance_saving_account,
            total_items=len(balance_saving_account)
        )

    async def get_detail_reset_password_teller(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password_teller(cif_id))

        return self.response(data=detail_reset_password_data)
