from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.e_banking.repository import (
    repos_balance_saving_account_data, repos_check_e_banking,
    repos_get_detail_reset_password, repos_get_detail_reset_password_teller,
    repos_get_e_banking_data, repos_get_list_balance_payment_account,
    repos_save_e_banking_data
)
from app.api.v1.endpoints.cif.e_banking.schema import (
    EBankingRequest, GetInitialPasswordMethod
)
from app.api.v1.endpoints.cif.repository import repos_get_initializing_customer
from app.third_parties.oracle.models.master_data.customer import (
    CustomerContactType, CustomerRelationshipType
)
from app.third_parties.oracle.models.master_data.e_banking import (
    EBankingNotification
)
from app.third_parties.oracle.models.master_data.others import (
    MethodAuthentication
)
from app.utils.constant.cif import (
    EBANKING_ACCOUNT_TYPE_CHECKING, EBANKING_ACTIVE_PASSWORD_EMAIL,
    EBANKING_ACTIVE_PASSWORD_SMS, EBANKING_HAS_FEE, EBANKING_HAS_NO_FEE
)
from app.utils.functions import dropdown, generate_uuid, now


class CtrEBanking(BaseController):
    async def ctr_save_e_banking(self, cif_id: str, e_banking: EBankingRequest):
        """
        func dùng để tạo mới E-banking phần (I, III.A)
        """

        data_reg_balance_option = []  # OTT/SMS
        data_eb_reg_balance = []  # dữ liệu thông tin người nhận thông báo (primary)
        data_eb_receiver_noti_relationship = []  # dữ liệu thông tin người nhận thông báo (relationship)
        data_eb_reg_balance_noti = []  # dư liệu tùy chọn thông báo
        data_account_info = {}  # Thông tin tài khoản
        auth_method = []  # Hình thức xác thực
        current_customer = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        # I. Thông tin biến động số dư tài khoản thanh toán
        change_of_balance_payment_account = e_banking.change_of_balance_payment_account

        if e_banking.change_of_balance_payment_account.register_flag:
            # kiểm tra hình thức liên lạc
            contact_types = await self.get_model_objects_by_ids(
                model=CustomerContactType,
                model_ids=[contact_type.id for contact_type in change_of_balance_payment_account.customer_contact_types
                           if contact_type.checked_flag],
                loc="change_of_balance_payment_account -> customer_contact_types"
            )

            register_balance_casas = change_of_balance_payment_account.register_balance_casas

            # kiểm tra tùy chọn thông báo, mối quan hệ
            notification_ids, relationship_ids, casa_account_ids = [], set(), []
            for register_balance_casa in register_balance_casas:
                for notification in register_balance_casa.e_banking_notifications:
                    notification_ids.append(notification.id)
                for relationship in register_balance_casa.notification_casa_relationships:
                    relationship_ids.add(relationship.relationship_type.id)
                casa_account_ids.append(register_balance_casa.account_id)

            # kiểm tra tùy chọn thông báo
            await self.get_model_objects_by_ids(
                model=EBankingNotification,
                model_ids=notification_ids,
                loc="change_of_balance_payment_account -> register_balance_casas -> e_banking_notifications"
            )

            # kiểm tra mối quan hệ
            await self.get_model_objects_by_ids(
                model=CustomerRelationshipType,
                model_ids=list(relationship_ids),
                loc="notification_casa_relationships -> relationship_type -> id"
            )

            # TODO kiểm tra tài khoản nhận thông báo, hiện tại mới tạo tài khoản thanh toán => chưa có account_id
            # if register_balance_casas.account_id:
            #     await self.get_model_objects_by_ids(
            #         model=CasaAccount,
            #         model_ids=casa_account_ids,
            #         loc="register_balance_casas -> account_id"
            #     )

            # Hình thức nhận thông báo
            for contact_type in contact_types:
                data_reg_balance_option.append({
                    "customer_id": cif_id,
                    "e_banking_register_account_type": EBANKING_ACCOUNT_TYPE_CHECKING,
                    "customer_contact_type_id": contact_type.id,
                    "created_at": now()
                })

            # Thông tin nhận thông báo
            for register_balance_casa in register_balance_casas:
                eb_reg_balance_id = generate_uuid()
                data_eb_reg_balance.append({
                    "id": eb_reg_balance_id,
                    "customer_id": cif_id,
                    "e_banking_register_account_type": EBANKING_ACCOUNT_TYPE_CHECKING,
                    "full_name": current_customer.full_name_vn,
                    "mobile_number": register_balance_casa.primary_phone_number,
                    "account_id": register_balance_casa.account_id,
                    "name": register_balance_casa.account_name,

                })
                for relationship in register_balance_casa.notification_casa_relationships:
                    data_eb_receiver_noti_relationship.append({
                        "e_banking_register_balance_casa_id": eb_reg_balance_id,
                        "relationship_type_id": relationship.relationship_type.id,
                        "mobile_number": relationship.mobile_number,
                        "full_name": relationship.full_name_vn
                    })
                # Tùy chọn nhận thông báo
                for notification in register_balance_casa.e_banking_notifications:
                    if notification.checked_flag:
                        data_eb_reg_balance_noti.append({
                            "eb_notify_id": notification.id,
                            "eb_reg_balance_id": eb_reg_balance_id

                        })

        # III. Thông tin e-banking
        # Thông tin tài khoản
        account_information = e_banking.e_banking_information.account_information
        if account_information.register_flag:
            # kiểm tra hình thức xác nhận mật khẩu lần đầu
            auth_method_ids = [method.id for method in account_information.method_authentication if method.checked_flag]
            auth_types = await self.get_model_objects_by_ids(
                model=MethodAuthentication,
                model_ids=auth_method_ids,
                loc="method_authentication -> id"
            )

            # List xác thực có HARD TOKEN => tốn phí
            has_fee = EBANKING_HAS_FEE if "HARD TOKEN" in [auth_type.name for auth_type in auth_types if
                                                           auth_type.active_flag] else EBANKING_HAS_NO_FEE

            method_active_password_id = EBANKING_ACTIVE_PASSWORD_EMAIL if \
                account_information.get_initial_password_method == GetInitialPasswordMethod.Email \
                else EBANKING_ACTIVE_PASSWORD_SMS

            e_banking_info_id = generate_uuid()
            data_account_info = {
                "id": e_banking_info_id,
                "customer_id": cif_id,
                "method_active_password_id": method_active_password_id,
                "account_name": account_information.account_name,
                "ib_mb_flag": account_information.register_flag,
                "method_payment_fee_flag": has_fee

            }

            # Hình thức xác thực
            for auth_method_id in auth_method_ids:
                auth_method.append({
                    "e_banking_info_id": e_banking_info_id,
                    "method_authentication_id": auth_method_id
                })
        e_banking_data = self.call_repos(
            await repos_save_e_banking_data(
                log_data=e_banking.json(),
                session=self.oracle_session,
                cif_id=cif_id,
                balance_option=data_reg_balance_option,
                reg_balance=data_eb_reg_balance,
                relationship=data_eb_receiver_noti_relationship,
                balance_noti=data_eb_reg_balance_noti,
                account_info=data_account_info,
                auth_method=auth_method,
                created_by=self.current_user.full_name_vn
            )
        )

        return self.response(data=e_banking_data)

    async def ctr_get_e_banking(self, cif_id: str):
        """
        1. Kiểm tra tồn tại của cif_id
        2. Kiểm tra cif_id đã có E-banking chưa
        3. Trả data E-banking
        """

        # 1. Kiểm tra tồn tại của cif_id
        _ = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session))

        # 2. Kiểm tra cif_id đã có E-banking chưa
        data_e_banking = await repos_check_e_banking(cif_id=cif_id, session=self.oracle_session)
        if not data_e_banking:
            return self.response_exception(
                msg='ERROR_E-BANKING',
                loc='cif_id not have E-Banking',
                detail=f'E-Banking -> cif_id -> {cif_id}'
            )

        # 3. Trả data E-banking
        data = self.call_repos(
            await repos_get_e_banking_data(
                cif_id=cif_id,
                session=self.oracle_session))

        contact_types = data['contact_types']
        data_e_banking = data['data_e_banking']
        e_bank_info = data['e_bank_info']

        checking_registration_info, saving_registration_info = {}, {}
        for register in data_e_banking:
            if register.EBankingRegisterBalance.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_CHECKING:
                if not checking_registration_info.get(register.EBankingRegisterBalance.account_id):
                    checking_registration_info[
                        register.EBankingRegisterBalance.account_id] = register.EBankingRegisterBalance.__dict__
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"] = [
                        register.EBankingNotification]
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"] = [{
                        "info": register.EBankingReceiverNotificationRelationship,
                        "relation_type": register.CustomerRelationshipType
                    }]
                else:
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"].append(
                        register.EBankingNotification)
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"].append({
                        "info": register.EBankingReceiverNotificationRelationship,
                        "relation_type": register.CustomerRelationshipType
                    })
            else:
                if not saving_registration_info.get(register.EBankingRegisterBalance.account_id):
                    saving_registration_info[
                        register.EBankingRegisterBalance.account_id] = register.EBankingRegisterBalance.__dict__
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"] = [
                        register.EBankingNotification]
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"] = [{
                        "info": register.EBankingReceiverNotificationRelationship,
                        "relation_type": register.CustomerRelationshipType
                    }]
                else:
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["notifications"].append(
                        register.EBankingNotification)
                    checking_registration_info[register.EBankingRegisterBalance.account_id]["relationships"].append({
                        "info": register.EBankingReceiverNotificationRelationship,
                        "relation_type": register.CustomerRelationshipType
                    })

        account_info = {}
        for auth_method in e_bank_info:
            if auth_method.EBankingInfo:
                account_info["register_flag"] = auth_method.EBankingInfo.ib_mb_flag
                account_info["account_name"] = auth_method.EBankingInfo.account_name
                account_info["charged_account"] = auth_method.EBankingInfo.account_payment_fee
                account_info["get_initial_password_method"] = GetInitialPasswordMethod(
                    auth_method.EBankingInfo.method_active_password_id)
                break
        data = {
            "change_of_balance_payment_account": {
                "register_flag": True if checking_registration_info else False,
                "customer_contact_types": [
                    {
                        "id": contact_type.CustomerContactType.id,
                        "name": contact_type.CustomerContactType.name,
                        "group": contact_type.CustomerContactType.group,
                        "description": contact_type.CustomerContactType.description,
                        "checked_flag": True if contact_type.EBankingRegisterBalanceOption else False
                    } for contact_type in contact_types if
                    contact_type.EBankingRegisterBalanceOption.e_banking_register_account_type == EBANKING_ACCOUNT_TYPE_CHECKING
                ],
                "register_balance_casas": [
                    {
                        "account_id": registration_info['account_id'],
                        "checking_account_name": registration_info['name'],
                        "primary_phone_number": registration_info.get('mobile_number'),
                        "full_name_vn": registration_info['full_name'],
                        "notification_casa_relationships": [
                            {
                                "id": relationship["info"].id,
                                "mobile_number": relationship["info"].mobile_number,
                                "full_name_vn": relationship["info"].full_name,
                                "relationship_type": dropdown(relationship["relation_type"])
                            } for relationship in registration_info['relationships']
                        ],
                        "e_banking_notifications": [
                            {
                                **dropdown(notification),
                                "checked_flag": True
                            } for notification in registration_info['notifications']
                        ]
                    } for registration_info in checking_registration_info.values()
                ]
            },
            "e_banking_information": {
                "account_information": {
                    **account_info,
                    "method_authentication": [
                        {
                            **dropdown(method.MethodAuthentication),
                            "checked_flag": True if method.EBankingInfo else False
                        } for method in e_bank_info
                    ],
                },
            }
        }

        return self.response(data=data)

    async def ctr_balance_payment_account(self, cif_id: str):
        is_success, payment_account = self.call_repos(
            await repos_get_list_balance_payment_account(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )
        response_data = []
        if payment_account:
            payment_accounts = payment_account['selectCurrentAccountFromCIF_out']['accountInfo']
            for account in payment_accounts:
                response_data.append({
                    "id": account['customerInfo']['rowOrder'],
                    "account_number": account['accountNum'],
                    "product_name": account['accountClassName'],
                })

        return self.response(data=response_data)

    async def get_detail_reset_password(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password(cif_id))

        return self.response(data=detail_reset_password_data)

    async def ctr_balance_saving_account(self, cif_id: str):
        is_success, balance_saving_account = self.call_repos(
            await repos_balance_saving_account_data(
                cif_id=cif_id,
                session=self.oracle_session
            )
        )

        response_data = []
        if balance_saving_account:
            balance_saving_accounts = balance_saving_account['selectDepositAccountFromCIF_out']['accountInfo']
            for account in balance_saving_accounts:
                response_data.append({
                    "id": account['customerInfo']['rowOrder'],
                    "account_number": account['accountNum'],
                    "name": account['customerInfo']['fullname'],
                })

        return self.response_paging(
            data=response_data,
            total_item=len(response_data)
        )

    async def get_detail_reset_password_teller(self, cif_id: str):
        detail_reset_password_data = self.call_repos(await repos_get_detail_reset_password_teller(cif_id))

        return self.response(data=detail_reset_password_data)
