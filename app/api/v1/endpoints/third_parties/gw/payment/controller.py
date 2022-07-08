from app.api.base.controller import BaseController
from app.api.v1.endpoints.approval.repository import (
    repos_get_booking_business_form_by_booking_id
)
from app.api.v1.endpoints.casa.transfer.repository import (
    repos_get_casa_transfer_info
)
from app.api.v1.endpoints.cif.repository import (
    repos_get_account_id_by_account_number
)
from app.api.v1.endpoints.config.bank.controller import CtrConfigBank
from app.api.v1.endpoints.third_parties.gw.payment.repository import (
    repos_create_booking_payment, repos_gw_pay_in_cash,
    repos_gw_payment_amount_block, repos_gw_payment_amount_unblock,
    repos_gw_redeem_account, repos_gw_save_casa_transfer_info,
    repos_pay_in_cash_247_by_acc_num, repos_payment_amount_block,
    repos_payment_amount_unblock
)
from app.api.v1.endpoints.third_parties.gw.payment.schema import (
    RedeemAccountRequest
)
from app.api.v1.others.booking.controller import CtrBooking
from app.api.v1.validator import validate_history_data
from app.settings.config import DATETIME_INPUT_OUTPUT_REVERT_FORMAT
from app.third_parties.oracle.models.master_data.bank import BankBranch
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK,
    BUSINESS_TYPE_REDEEM_ACCOUNT
)
from app.utils.constant.casa import (
    RECEIVING_METHOD_SCB_BY_IDENTITY, RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT
)
from app.utils.constant.cif import (
    BUSINESS_FORM_AMOUNT_BLOCK, BUSINESS_FORM_AMOUNT_UNBLOCK,
    PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK,
    PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.constant.gw import (
    GW_CASA_RESPONSE_STATUS_SUCCESS, GW_GL_BRANCH_CODE
)
from app.utils.functions import (
    datetime_to_string, now, orjson_dumps, orjson_loads
)


class CtrGWPayment(BaseController):

    async def ctr_payment_amount_block(
            self,
            BOOKING_ID: str,
            account_amount_blocks: list
    ):
        current_user = self.current_user # noqa

        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=BOOKING_ID,
            business_type_code=BUSINESS_TYPE_AMOUNT_BLOCK,
            check_correct_booking_flag=False,
            loc=f'booking_id: {BOOKING_ID}'
        )
        request_datas = []
        account_numbers = []
        for item in account_amount_blocks:
            account_numbers.append(item.account_number)
            request_datas.append({
                "account_info": {
                    "account_num": item.account_number
                },
                "p_blk_detail": {
                    "AMOUNT": item.amount,
                    "AMOUNT_BLOCK_TYPE": item.amount_block_type,
                    "HOLD_CODE": item.hold_code,
                    "EFFECTIVE_DATE": item.effective_date,
                    "EXPIRY_DATE": item.expiry_date if item.expiry_date else "",
                    "REMARKS": item.remarks,
                    "VERIFY_AVAILABLE_BALANCE": item.verify_available_balance,
                    "CHARGE_DETAIL": {
                        "TYPE_CHARGE": "",
                        "ACCOUNT_CHARGE": ""
                    }
                },
                # TODO chưa được mô tả
                "p_blk_charge": [
                    {
                        "CHARGE_NAME": "",
                        "CHARGE_AMOUNT": 0,
                        "WAIVED": "N"
                    }
                ],
                # TODO chưa được mô tả
                "p_blk_udf": [
                    {
                        "UDF_NAME": "",
                        "UDF_VALUE": "",
                        "AMOUNT_BLOCK": {
                            "UDF_NAME": "",
                            "UDF_VALUE": ""
                        }
                    }
                ],
                "staff_info_checker": {
                    # TODO hard core
                    "staff_name": "HOANT2"
                },
                "staff_info_maker": {
                    # TODO hard core
                    "staff_name": "KHANHLQ"
                }
            })

        if len(set(account_numbers)) != len(account_amount_blocks):
            return self.response_exception(msg="account_number duplicate")

        saving_booking_account = []
        saving_booking_customer = [] # noqa

        for account_number in account_numbers:
            # TODO check account_number in db crm
            response_data = self.call_repos(
                await repos_get_account_id_by_account_number(
                    account_number=account_number,
                    session=self.oracle_session
                ))

            saving_booking_account.append({
                "booking_id": BOOKING_ID,
                "account_id": response_data.get('account_id'),
                "created_at": now()
            })

            saving_booking_customer.append({
                "booking_id": BOOKING_ID,
                "customer_id": response_data.get('customer_id')
            })
        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_BLOCK,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user.user_info
        )

        # Validate history data
        is_success, history_response = validate_history_data(history_datas)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        # Tạo data TransactionDaily và các TransactionStage
        transaction_datas = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_AMOUNT_BLOCK,
            booking_id=BOOKING_ID,
            request_json=orjson_dumps(request_datas),
            history_datas=orjson_dumps(history_datas),
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_datas

        booking_id = self.call_repos(await repos_payment_amount_block(
            booking_id=BOOKING_ID,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            saving_transaction_job=saving_transaction_job,
            saving_booking_business_form=saving_booking_business_form,
            saving_booking_account=saving_booking_account,
            saving_booking_customer=saving_booking_customer,
            session=self.oracle_session
        ))
        response_data = {
            "booking_id": booking_id
        }

        return self.response(data=response_data)

    async def ctr_gw_payment_amount_block(self, BOOKING_ID: str):
        current_user = self.current_user

        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=BOOKING_ID,
                business_form_id=BUSINESS_FORM_AMOUNT_BLOCK,
                session=self.oracle_session

            ))

        request_data_gw = orjson_loads(booking_business_form.form_data)

        gw_payment_amount_block = self.call_repos(await repos_gw_payment_amount_block(
            current_user=current_user,
            booking_id=BOOKING_ID,
            request_data_gw=request_data_gw,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": BOOKING_ID,
            "account_list": gw_payment_amount_block
        }

        return self.response(data=response_data)

    async def ctr_payment_amount_unblock(
            self,
            BOOKING_ID: str,
            account_amount_unblocks: list
    ):
        # Kiểm tra booking
        await CtrBooking().ctr_get_booking_and_validate(
            booking_id=BOOKING_ID,
            business_type_code=BUSINESS_TYPE_AMOUNT_UNBLOCK,
            check_correct_booking_flag=False,
            loc=f'booking_id: {BOOKING_ID}'
        )

        current_user = self.current_user
        request_data = []
        account_ref = []
        account_numbers = []
        for account_number in account_amount_unblocks:
            if account_number.account_number in account_numbers:
                return self.response_exception(msg="Duplicate Account_number", detail=f"Account_number {account_number.account_number}")

            account_numbers.append(account_number.account_number)
            p_blk_detail = {
                "AMOUNT": "",
                "HOLD_CODE": "",
                "EXPIRY_DATE": "",
                "REMARKS": "",
                "CHARGE_DETAIL": {
                    "TYPE_CHARGE": "",
                    "ACCOUNT_CHARGE": ""
                }
            }
            for account_amount in account_number.account_amount_block:
                if account_amount.account_ref_no in account_ref:
                    return self.response_exception(msg="Duplicate Account_ref", detail=f"Account_ref {account_amount.account_ref_no}")
                account_ref.append(account_amount.account_ref_no)
                if account_amount.p_type_unblock == "P":
                    if not account_amount.p_blk_detail:
                        return self.response_exception(msg="type_unblock is not data")

                    p_blk_detail = {
                        "AMOUNT": account_amount.p_blk_detail.amount,
                        "HOLD_CODE": account_amount.p_blk_detail.hold_code,
                        "EXPIRY_DATE": account_amount.p_blk_detail.expiry_date,
                        "REMARKS": account_amount.p_blk_detail.remarks,
                        "CHARGE_DETAIL": {
                            "TYPE_CHARGE": "",
                            "ACCOUNT_CHARGE": ""
                        }
                    }

                request_data.append({
                    "account_info": {
                        "balance_lock_info": {
                            "account_ref_no": account_amount.account_ref_no
                        }
                    },
                    "p_type_unblock": account_amount.p_type_unblock,
                    "p_blk_detail": p_blk_detail,
                    # TODO hard core
                    "p_blk_charge": [
                        {
                            "CHARGE_NAME": "",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    # TODO hard core
                    "p_blk_udf": [
                        {
                            "UDF_NAME": "",
                            "UDF_VALUE": "",
                            "AMOUNT_UNBLOCK": {
                                "UDF_NAME": "",
                                "UDF_VALUE": ""
                            }
                        }
                    ],
                    "staff_info_checker": {
                        # TODO hard core
                        "staff_name": "HOANT2"
                    },
                    "staff_info_maker": {
                        # TODO hard core
                        "staff_name": "KHANHLQ"
                    }
                })

        saving_booking_account = []
        saving_booking_customer = []

        for account_number in account_numbers:
            # TODO check account_number in db crm
            response_data = self.call_repos(
                await repos_get_account_id_by_account_number(
                    account_number=account_number,
                    session=self.oracle_session
                ))
            saving_booking_account.append({
                "booking_id": BOOKING_ID,
                "account_id": response_data.get('account_id'),
                "created_at": now()
            })

            saving_booking_customer.append({
                "booking_id": BOOKING_ID,
                "customer_id": response_data.get('customer_id')
            })

        history_data = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_AMOUNT_UNBLOCK,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user.user_info
        )

        # Validate history data
        is_success, history_response = validate_history_data(history_data)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        # Tạo data TransactionDaily và các TransactionStage
        transaction_data = await self.ctr_create_transaction_daily_and_transaction_stage_for_init(
            business_type_id=BUSINESS_TYPE_AMOUNT_UNBLOCK,
            booking_id=BOOKING_ID,
            request_json=orjson_dumps(request_data),
            history_datas=orjson_dumps(history_data),
        )
        (
            saving_transaction_stage_status, saving_sla_transaction, saving_transaction_stage,
            saving_transaction_stage_phase, saving_transaction_stage_lane, saving_transaction_stage_role,
            saving_transaction_daily, saving_transaction_sender, saving_transaction_job, saving_booking_business_form
        ) = transaction_data

        booking_id = self.call_repos(await repos_payment_amount_unblock(
            booking_id=BOOKING_ID,
            saving_transaction_stage_status=saving_transaction_stage_status,
            saving_sla_transaction=saving_sla_transaction,
            saving_transaction_stage=saving_transaction_stage,
            saving_transaction_stage_phase=saving_transaction_stage_phase,
            saving_transaction_stage_lane=saving_transaction_stage_lane,
            saving_transaction_stage_role=saving_transaction_stage_role,
            saving_transaction_daily=saving_transaction_daily,
            saving_transaction_sender=saving_transaction_sender,
            saving_transaction_job=saving_transaction_job,
            saving_booking_business_form=saving_booking_business_form,
            saving_booking_account=saving_booking_account,
            saving_booking_customer=saving_booking_customer,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": booking_id,
        }
        return self.response(data=response_data)

    async def ctr_gw_payment_amount_unblock(
            self,
            BOOKING_ID: str,
    ):
        current_user = self.current_user
        booking_business_form = self.call_repos(
            await repos_get_booking_business_form_by_booking_id(
                booking_id=BOOKING_ID,
                business_form_id=BUSINESS_FORM_AMOUNT_UNBLOCK,
                session=self.oracle_session

            ))
        request_data = orjson_loads(booking_business_form.form_data)

        gw_payment_amount_unblock = self.call_repos(await repos_gw_payment_amount_unblock(
            current_user=current_user,
            booking_id=BOOKING_ID,
            request_data_gw=request_data,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": BOOKING_ID,
            "account_list": gw_payment_amount_unblock
        }
        return self.response(data=response_data)

    async def ctr_gw_redeem_account(self, redeem_account: RedeemAccountRequest):
        current_user = self.current_user
        payout_details = [{
            "payout_component": item.payout_component,
            "payout_mode": item.payout_mode,
            "payout_amount": item.payout_amount,
            "offset_account": item.offset_account
        } for item in redeem_account.p_payout_detail.payout_details]
        data_input = {
            "account_info": {
                "account_num": redeem_account.account_info.account_number,
            },
            "p_payout_detail": {
                "redemption_details": {
                    "redemption_mode": redeem_account.p_payout_detail.redemption_details.redemption_mode,
                    "redemption_amount": redeem_account.p_payout_detail.redemption_details.redemption_amount,
                    "waive_penalty": redeem_account.p_payout_detail.redemption_details.waive_penalty,
                    "waive_interest": redeem_account.p_payout_detail.redemption_details.waive_interest
                },
                "payout_details": payout_details
            },
            # TODO hard core
            "p_denominated_deposit": "",
            "p_addl_payout_detail": "",
            "p_charges": "",
            "p_denomination": "",
            "p_mis": "",
            "p_udf": [
                {
                    "UDF_NAME": "",
                    "UDF_VALUE": ""
                }
            ],
            # TODO hard core
            "staff_info_checker": {
                "staff_name": "HOANT2"
            },
            # TODO hard core
            "staff_info_maker": {
                "staff_name": "KHANHLQ"
            }
        }
        request_data, gw_payment_redeem_account = self.call_repos(
            await repos_gw_redeem_account(
                current_user=current_user,
                data_input=data_input,
            )
        )

        booking_id, booking_code = self.call_repos(await repos_create_booking_payment(
            business_type_code=BUSINESS_TYPE_REDEEM_ACCOUNT,
            current_user=current_user.user_info,
            form_data=request_data,
            log_data=gw_payment_redeem_account,
            session=self.oracle_session
        ))

        redeem_account = gw_payment_redeem_account.get('redeemAccount_out', {})
        # check trường hợp lỗi
        if redeem_account.get('transaction_info').get('transaction_error_code') != GW_CASA_RESPONSE_STATUS_SUCCESS:
            return self.response_exception(msg=redeem_account.get('transaction_info').get('transaction_error_msg'))
        response_data = {
            "booking_id": booking_id,
        }
        return self.response(data=response_data)

    ####################################################################################################################
    # Nộp tiền
    ####################################################################################################################
    async def ctr_gw_pay_in_cash(
            self,
            form_data
    ):
        current_user = self.current_user
        sender_place_of_issue_id = form_data['sender_place_of_issue']['id']
        sender_place_of_issue = await self.get_model_object_by_id(
            model_id=sender_place_of_issue_id,
            model=PlaceOfIssue,
            loc=f"sender_place_of_issue_id: {sender_place_of_issue_id}"
        )

        data_input = {
            "account_info": {
                # "account_num": form_data['receiver_account_number'],
                "account_num": form_data['receiver_account_number'],
                "account_currency": "VND",  # TODO: hiện tại chuyển tiền chỉ dùng tiền tệ VN
                "account_opening_amount": form_data['amount']
            },
            "p_blk_denomination": "",
            "p_blk_charge": [
                {
                    "CHARGE_TYPE": "CASH",
                    "CHARGE_ACCOUNT": "",
                    "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                    "CHARGE_AMOUNT": 100000,
                    "WAIVED": "N"
                }
            ],
            "p_blk_project": "",
            "p_blk_mis": "",
            "p_blk_udf": [
                {
                    "UDF_NAME": "NGUOI_GIAO_DICH",
                    "UDF_VALUE": self.current_user.user_info.name
                },
                {
                    "UDF_NAME": "CMND_PASSPORT",
                    "UDF_VALUE": form_data['sender_identity_number']
                },
                {
                    "UDF_NAME": "NGAY_CAP",
                    "UDF_VALUE": form_data['sender_issued_date']
                },
                {
                    "UDF_NAME": "NOI_CAP",
                    "UDF_VALUE": sender_place_of_issue.name
                },
                {
                    "UDF_NAME": "DIA_CHI",
                    "UDF_VALUE": form_data['sender_address_full']
                },
                {
                    "UDF_NAME": "THU_PHI_DICH_VU",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "TEN_KHACH_HANG",
                    "UDF_VALUE": form_data['sender_full_name_vn']
                },
                {
                    "UDF_NAME": "TY_GIA_GD_DOI_UNG_HO",
                    "UDF_VALUE": "1"
                },
                {
                    "UDF_NAME": "MUC_DICH_GIAO_DICH",
                    "UDF_VALUE": "MUC_DICH_KHAC"
                },
                {
                    "UDF_NAME": "NGHIEP_VU_GDQT",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "NGAY_CHOT_TY_GIA",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "GIO_PHUT_CHOT_TY_GIA",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_1",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_2",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_3",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_4",
                    "UDF_VALUE": ""
                },
                {
                    "UDF_NAME": "REF_BAO_CO_5",
                    "UDF_VALUE": ""
                }
            ],
            "staff_info_checker": {
                "staff_name": "HOANT2"
            },
            "staff_info_maker": {
                "staff_name": "KHANHLQ"
            }
        }
        gw_pay_in_cash = self.call_repos(await repos_gw_pay_in_cash(
            data_input=data_input,
            current_user=current_user
        ))
        return self.response(data=gw_pay_in_cash)

    async def ctr_gw_pay_in_cash_247_by_acc_num(
            self,
            booking_id: str,
            form_data: dict
    ):
        current_user = self.current_user
        current_user_info = current_user.user_info

        ben = await CtrConfigBank(current_user).ctr_get_bank_branch(bank_id=form_data['receiver_bank']['id'])

        data_input = {
            "customer_info": {
                "full_name": form_data['sender_full_name_vn'],
                "birthday": form_data['sender_issued_date']  # TODO
            },
            "id_info": {
                "id_num": form_data['sender_identity_number']
            },
            "address_info": {
                "address_full": form_data['sender_address_full']
            },
            "trans_date": datetime_to_string(now()),
            "time_stamp": datetime_to_string(now()),
            "trans_id": booking_id,
            "amount": form_data['amount'],
            "description": form_data['content'],
            "account_to_info": {
                "account_num": form_data['receiver_account_number']
            },
            "ben_id": ben['data'][0]['id'],
            "account_from_info": {
                "account_num": GW_GL_BRANCH_CODE
            },
            "staff_maker": {
                "staff_code": "annvh"   # TODO
            },
            "staff_checker": {
                "staff_code": "THUYTP"  # TODO
            },
            "branch_info": {
                "branch_code": current_user_info.hrm_branch_code
            }
        }
        gw_pay_in_cash = self.call_repos(await repos_pay_in_cash_247_by_acc_num(
            data_input=data_input,
            current_user=current_user
        ))
        return self.response(data=gw_pay_in_cash)

    async def ctr_gw_save_casa_transfer_info(self, BOOKING_ID: str):
        get_casa_transfer_info = self.call_repos(await repos_get_casa_transfer_info(
            booking_id=BOOKING_ID,
            session=self.oracle_session
        ))
        form_data = orjson_loads(get_casa_transfer_info.form_data)

        receiving_method = form_data['receiving_method']
        transfer_amount = form_data['amount']

        # Thông tin phí
        ################################################################################################################
        fee_info = form_data['fee_info']
        fee_amount = fee_info['fee_amount']
        vat_tax = fee_amount / 10
        total = fee_amount + vat_tax
        actual_total = int(total + transfer_amount)

        request_data = {}

        if receiving_method == RECEIVING_METHOD_SCB_TO_ACCOUNT:
            request_data = {
                "data_input": {
                    "p_blk_detail": {
                        "FROM_ACCOUNT_DETAILS": {
                            "FROM_ACCOUNT_NUMBER": form_data['sender_account_number'],
                            "FROM_ACCOUNT_AMOUNT": actual_total
                        },
                        "TO_ACCOUNT_DETAILS": {
                            "TO_ACCOUNT_NUMBER": form_data['receiver_account_number']
                        }
                    },
                    "p_blk_charge": [],  # TODO thông tin phí
                    "p_blk_mis": "",
                    "p_blk_udf": [
                        {
                            "UDF_NAME": "",
                            "UDF_VALUE": ""
                        }
                    ],
                    "p_blk_project": "",
                    # TODO
                    "staff_info_checker": {
                        "staff_name": "HOANT2"
                    },
                    # TODO
                    "staff_info_maker": {
                        "staff_name": "KHANHLQ"
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_SCB_BY_IDENTITY and \
                receiving_method == RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY:
            request_data = {
                "data_input": {
                    "p_liquidation_type": "C",
                    "p_liquidation_details": "",
                    "branch_info": {
                        "branch_code": "001"
                    },
                    "p_instrument_number": "123245678",
                    "p_instrument_status": "LIQD",
                    "account_info": {
                        "account_num": "123456787912",
                        "account_currency": "VND"
                    },
                    "p_charges": [
                        {
                            "CHARGE_NAME": "",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    "p_mis": "",
                    "p_udf": [
                        {
                            "UDF_NAME": "",
                            "UDF_VALUE": ""
                        }
                    ],
                    "staff_info_checker": {
                        "staff_name": "HOANT2"
                    },
                    "staff_info_maker": {
                        "staff_name": "KHANHLQ"
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT:
            bank_id = form_data['receiver_bank']['id']
            bank_info = await self.get_model_object_by_id(model_id=bank_id, model=BankBranch, loc='receiver_bank_id')
            request_data = {
                "data_input": {
                    "account_info": {
                        "account_bank_code": bank_info.code,
                        "account_product_package": "FT01"
                    },
                    "staff_info_checker": {
                        "staff_name": "HOANT2"
                    },
                    "staff_info_maker": {
                        "staff_name": "KHANHLQ"
                    },
                    "p_blk_mis": "",
                    "p_blk_udf": "",
                    "p_blk_refinance_rates": "",
                    "p_blk_amendment_rate": "",
                    "p_blk_main": {
                        "PRODUCT": {
                            "DETAILS_OF_CHARGE": "Y" if fee_info['is_transfer_payer'] else "O",
                            "PAYMENT_FACILITY": "O"
                        },
                        "TRANSACTION_LEG": {
                            "ACCOUNT": form_data['sender_account_number'],
                            "AMOUNT": actual_total
                        },
                        "RATE": {
                            "EXCHANGE_RATE": 0,
                            "LCY_EXCHANGE_RATE": 0,
                            "LCY_AMOUNT": 0
                        },
                        "ADDITIONAL_INFO": {
                            "RELATED_CUSTOMER": form_data["sender_cif_number"],
                            "NARRATIVE": form_data["content"]
                        }
                    },
                    "p_blk_charge": [
                        {
                            "CHARGE_NAME": "PHI DV TT TRONG NUOC  711003001",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        },
                        {
                            "CHARGE_NAME": "THUE VAT",
                            "CHARGE_AMOUNT": 0,
                            "WAIVED": "N"
                        }
                    ],
                    "p_blk_settlement_detail": {
                        "SETTLEMENTS": {
                            "TRANSFER_DETAIL": {
                                "BENEFICIARY_ACCOUNT_NUMBER": form_data['receiver_account_number'],
                                "BENEFICIARY_NAME": form_data['receiver_fullname_vn'],
                                "BENEFICIARY_ADRESS": form_data['receiver_province']['name'],
                                "ID_NO": "",
                                "ISSUE_DATE": "",
                                "ISSUER": ""
                            },
                            "ORDERING_CUSTOMER": {
                                "ORDERING_ACC_NO": form_data['receiver_account_number'],
                                "ORDERING_NAME": form_data['receiver_fullname_vn'],
                                "ORDERING_ADDRESS": form_data['receiver_province']['name'],
                                "ID_NO": "",
                                "ISSUE_DATE": "",
                                "ISSUER": ""
                            }
                        }
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_TO_ACCOUNT:
            request_data = {
                "data_input": {
                    "ben_id": "970436",
                    "trans_date": datetime_to_string(_time=now()),
                    "time_stamp": datetime_to_string(_time=now(), _format=DATETIME_INPUT_OUTPUT_REVERT_FORMAT),
                    "trans_id": "20220629160002159368",
                    "amount": actual_total,
                    "description": form_data["content"],
                    "account_to_info": {
                        "account_num": form_data["receiver_account_number"]
                    },
                    "account_from_info": {
                        "account_num": form_data["sender_account_number"]
                    },
                    "customer_info": {
                        "full_name": form_data["sender_fullname_vn"]
                    },
                    # TODO
                    "staff_maker": {
                        "staff_code": "annvh"
                    },
                    # TODO
                    "staff_checker": {
                        "staff_code": "THUYTP"
                    },
                    # TODO
                    "branch_info": {
                        "branch_code": "001"
                    }
                }
            }

        if receiving_method == RECEIVING_METHOD_THIRD_PARTY_247_TO_CARD:
            request_data = {
                "data_input": {
                    "ben_id": "970436",
                    "trans_date": datetime_to_string(_time=now()),
                    "time_stamp": datetime_to_string(_time=now(), _format=DATETIME_INPUT_OUTPUT_REVERT_FORMAT),
                    "trans_id": "20220629160002159368",
                    "amount": int(actual_total),
                    "description": form_data["content"],
                    "account_from_info": {
                        "account_num": form_data["sender_account_number"]
                    },
                    "customer_info": {
                        "full_name": form_data["sender_full_name_vn"]
                    },
                    # TODO
                    "staff_maker": {
                        "staff_code": "annvh"
                    },
                    # TODO
                    "staff_checker": {
                        "staff_code": "THUYTP"
                    },
                    # TODO
                    "branch_info": {
                        "branch_code": "001"
                    },
                    "card_to_info": {
                        "card_num": form_data["receiver_card_number"]
                    }
                }
            }

        self.call_repos(await repos_gw_save_casa_transfer_info(
            current_user=self.current_user,
            receiving_method=receiving_method,
            booking_id=BOOKING_ID,
            request_data=request_data,
            session=self.oracle_session
        ))

        response_data = {
            "booking_id": BOOKING_ID,
        }
        return self.response(data=response_data)
    ####################################################################################################################
