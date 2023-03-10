from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.base.controller import BaseController
from app.api.v1.endpoints.cif.debit_card.repository import (
    get_data_debit_card_by_cif_num, repos_add_debit_card, repos_debit_card
)
from app.api.v1.endpoints.cif.debit_card.schema import DebitCardRequest
from app.api.v1.endpoints.cif.repository import (
    repos_get_booking, repos_get_initializing_customer
)
from app.api.v1.endpoints.third_parties.gw.card_works.controller import (
    CtrGWCardWorks
)
from app.api.v1.endpoints.third_parties.gw.customer.controller import (
    CtrGWCustomer
)
from app.api.v1.validator import validate_history_data
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.address import (
    AddressDistrict, AddressProvince, AddressWard
)
from app.third_parties.oracle.models.master_data.card import (
    BrandOfCard, CardAnnualFee, CardCustomerType, CardIssuanceFee,
    CardIssuanceType, CardType
)
from app.third_parties.oracle.models.master_data.others import Branch
from app.utils.constant.cif import (
    PROFILE_HISTORY_DESCRIPTIONS_INIT_DEBIT_CARD, PROFILE_HISTORY_STATUS_INIT
)
from app.utils.constant.debit_card import (
    GW_CARD_IS_PRIMARY_CARD, GW_CARD_IS_SUB_CARD, GW_CARD_STATUS_IN_USE,
    GW_DEFAULT_SUB_CARD_CHANEL
)
from app.utils.error_messages import (
    ERROR_CIF_NUMBER_NOT_EXIST, ERROR_NOT_REGISTER, VALIDATE_ERROR
)
from app.utils.functions import generate_uuid, now, orjson_dumps
from app.utils.vietnamese_converter import convert_to_unsigned_vietnamese


class CtrDebitCard(BaseController):
    async def ctr_debit_card(self, cif_id: str):

        debit_card = self.call_repos(await repos_debit_card(cif_id, self.oracle_session))

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))
        debit_card.update(booking=dict(
            id=booking.id,
            code=booking.code,
        ))
        return self.response(debit_card)

    async def ctr_add_debit_card(
            self,
            cif_id: str,
            debt_card_req: DebitCardRequest
    ):
        current_user = self.current_user.user_info
        # check register_flag == False thì ko insert data
        if not debt_card_req.issue_debit_card.register_flag:
            return self.response_exception(msg=ERROR_NOT_REGISTER,
                                           loc="debt_card_req -> issue_debit_card -> register_flag")

        # check, get current customer
        current_customer = self.call_repos(
            await repos_get_initializing_customer(
                cif_id=cif_id,
                session=self.oracle_session
            ))

        # convert last name, first name to unsigned vietnamese
        last_name = convert_to_unsigned_vietnamese(
            current_customer.last_name
        )
        first_name = convert_to_unsigned_vietnamese(
            current_customer.first_name
        )

        # Nếu cif_id tồn tại thi cập nhật lại data
        data_cards = self.call_repos(await get_data_debit_card_by_cif_num(self.oracle_session, cif_id))
        list_sub_card_ids = []
        list_card_type = []
        list_delivery_address_ids = []
        main_card_id = None
        if len(data_cards) > 0:
            for debit_card in data_cards:
                list_card_type.append(debit_card.id)
                list_delivery_address_ids.append(debit_card.card_delivery_address_id)
                if not debit_card.parent_card_id:
                    main_card_id = debit_card.id
                list_sub_card_ids.append(debit_card.id)

        """
            I. validate physical_card_type
                 1. check Constant
                 2. check số lượng nhỏ hơn 2
                 3. check trùng loạis

        """
        card_type = []
        for debt_card_type in debt_card_req.issue_debit_card.physical_card_type:
            card_type.append(debt_card_type.id)
        if len(card_type) > 2 or len(card_type) < 1:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="Number physical_card_type must be greater than 0 and less than 2",
                loc="issue_debit_card -> physical_card_type"
            )
        if len(card_type) != len(set(card_type)):
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="Data is duplicate",
                loc="issue_debit_card -> physical_card_type"
            )

        # check CardType exist
        await self.get_model_objects_by_ids(
            model=CardType,
            model_ids=list(card_type),
            loc="issue_debit_card -> physical_issuance_type -> id",
        )

        """Kiểm tra physical_issuance_type exist"""
        await self.get_model_object_by_id(
            model=CardIssuanceType,
            model_id=debt_card_req.issue_debit_card.physical_issuance_type.id,
            loc="issue_debit_card -> physical_issuance_type -> id",
        )

        """Kiểm tra customer_type"""
        await self.get_model_object_by_id(
            model=CardCustomerType,
            model_id=debt_card_req.issue_debit_card.customer_type.id,
            loc="issue_debit_card -> customer_type -> id",
        )

        """Kiểm tra branch_of_card"""
        await self.get_model_object_by_id(
            model=BrandOfCard,
            model_id=debt_card_req.issue_debit_card.branch_of_card.id,
            loc="issue_debit_card -> branch_of_card -> id",
        )

        """Kiểm tra issuance_fee"""
        await self.get_model_object_by_id(
            model=CardIssuanceFee,
            model_id=debt_card_req.issue_debit_card.issuance_fee.id,
            loc="issue_debit_card -> issuance fee -> id",
        )

        """Kiểm tra annual_fee"""
        await self.get_model_object_by_id(
            model=CardAnnualFee,
            model_id=debt_card_req.issue_debit_card.annual_fee.id,
            loc="issue_debit_card -> annual fee -> id",
        )

        """Validate first_name không None"""
        if not first_name or first_name.strip() == "":
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="first_name is null",
                loc="ctr_add_debit_card -> first_name"
            )

        """Validate last_name không None"""
        if not last_name or last_name.strip() == "":
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="last_name is null",
                loc="ctr_add_debit_card -> last_name"
            )

        """Validate tên dập nổi không quá 21 kí tự"""
        lenght_name = len(first_name + last_name)
        if first_name.upper() != debt_card_req.information_debit_card.name_on_card.first_name_on_card.upper():
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="first_name_on_card is wrong",
                loc="issue_debit_card -> information_debit_card -> name_on_card -> first_name_on_card"
            )
        if last_name.upper() != debt_card_req.information_debit_card.name_on_card.last_name_on_card.upper():
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="last_name_on_card is wrong",
                loc="issue_debit_card -> information_debit_card -> name_on_card -> last_name_on_card"
            )
        if debt_card_req.information_debit_card.name_on_card.middle_name_on_card:
            lenght_name = lenght_name + len(debt_card_req.information_debit_card.name_on_card.middle_name_on_card)

        if lenght_name > 21:
            return self.response_exception(
                msg=VALIDATE_ERROR,
                detail="Name on card is too long",
                loc="issue_debit_card -> information_debit_card -> name_on_card -> middle_name_on_card"
            )

        """Validate địa chỉ nhận thẻ"""
        if not debt_card_req.card_delivery_address.delivery_address_flag:
            # check Branch exist
            if not debt_card_req.card_delivery_address.scb_branch:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="scb_branch is null",
                    loc="card_delivery_address -> scb_branch"
                )
            await self.get_model_object_by_id(
                model=Branch,
                model_id=debt_card_req.card_delivery_address.scb_branch.id,
                loc="card_delivery_address -> scb_branch -> id",
            )
        else:
            if not debt_card_req.card_delivery_address.delivery_address:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="delivery_address is null",
                    loc="card_delivery_address -> delivery_address"
                )
            # check province
            await self.get_model_object_by_id(
                model=AddressProvince,
                model_id=debt_card_req.card_delivery_address.delivery_address.province.id,
                loc="card_delivery_address -> delivery_address -> province -> id",
            )
            # check district
            await self.get_model_object_by_id(
                model=AddressDistrict,
                model_id=debt_card_req.card_delivery_address.delivery_address.district.id,
                loc="card_delivery_address -> delivery_address -> district -> id",
            )
            # check ward
            await self.get_model_object_by_id(
                model=AddressWard,
                model_id=debt_card_req.card_delivery_address.delivery_address.ward.id,
                loc="card_delivery_address -> delivery_address -> ward -> id",
            )

            if not debt_card_req.card_delivery_address.delivery_address.number_and_street:
                return self.response_exception(
                    msg=VALIDATE_ERROR,
                    detail="number_and_street is null",
                    loc="card_delivery_address -> delivery_address -> number_and_street"
                )

        id_primary_card = generate_uuid()
        list_sub_delivery_address = []
        list_sub_debit_card = []
        list_sub_debit_card_type = []

        """Kiểm tra validate thông tin thẻ phụ"""
        if debt_card_req.information_sub_debit_card is not None:
            for index, sub_card in enumerate(debt_card_req.information_sub_debit_card.sub_debit_cards):
                if not CtrGWCustomer().ctr_gw_check_exist_customer_detail_info(cif_number=sub_card.cif_number,
                                                                               return_raw_data_flag=True):
                    return self.response_exception(
                        msg=ERROR_CIF_NUMBER_NOT_EXIST,
                        loc="information_sub_debit_card -> sub_debit_cards -> cif_number"
                    )

                # sub_customer_ids = self.call_repos(await get_data_customer_id(self.oracle_session, sub_card.cif_number))

                """Kiểm tra sub physical_card_type (Tính vật lý) tồn tại"""
                sub_card_type = []
                for item_card_type in sub_card.physical_card_type:
                    sub_card_type.append(item_card_type.id)
                if len(sub_card_type) > 2 or len(sub_card_type) < 1:
                    return self.response_exception(
                        msg=VALIDATE_ERROR,
                        detail="Number physical_card_type must be greater than 0 and less than 2",
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> physical_card_type"
                    )
                if len(sub_card_type) != len(set(sub_card_type)):
                    return self.response_exception(
                        msg=VALIDATE_ERROR,
                        detail="Data is duplicate",
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> physical_card_type -> 1"
                    )

                for idx, _ in enumerate(sub_card.physical_card_type):
                    await self.get_model_object_by_id(
                        model_id=_.id,
                        model=CardType,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> physical_card_type"
                            f" -> {idx} -> id",
                    )

                """Kiểm tra physical_issuance_type (Hình thức phát hành thẻ) exist"""
                await self.get_model_object_by_id(
                    model=CardIssuanceType,
                    model_id=sub_card.card_issuance_type.id,
                    loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_issuance_type -> id",
                )

                """Validate địa chỉ nhận thẻ"""
                if not sub_card.card_delivery_address.delivery_address_flag:
                    # Kiểm tra Branch exist
                    if not sub_card.card_delivery_address.scb_branch:
                        return self.response_exception(
                            msg=VALIDATE_ERROR,
                            detail="scb_branch is null",
                            loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address "
                                f"-> scb_branch "
                        )
                    await self.get_model_object_by_id(
                        model=Branch,
                        model_id=sub_card.card_delivery_address.scb_branch.id,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> "
                            f"scb_branch -> id",
                    )
                else:
                    if not sub_card.card_delivery_address.delivery_address:
                        return self.response_exception(
                            msg=VALIDATE_ERROR,
                            detail="delivery_address is null",
                            loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address "
                                f"-> delivery_address "
                        )
                    # check province
                    await self.get_model_object_by_id(
                        model=AddressProvince,
                        model_id=sub_card.card_delivery_address.delivery_address.province.id,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> "
                            f"province -> id",
                    )
                    # check district
                    await self.get_model_object_by_id(
                        model=AddressDistrict,
                        model_id=sub_card.card_delivery_address.delivery_address.district.id,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> "
                            f"district -> id",
                    )
                    # check ward
                    await self.get_model_object_by_id(
                        model=AddressWard,
                        model_id=sub_card.card_delivery_address.delivery_address.ward.id,
                        loc=f"information_sub_debit_card -> sub_debit_cards -> {index} -> card_delivery_address -> "
                            f"ward -> id",
                    )

                sub_uuid = generate_uuid()
                # neu scb_delivery_address_flag la True thi dia chi nhan la SCB
                if sub_card.card_delivery_address.delivery_address_flag is False:
                    # dia chi nhan (the phu)
                    sub_delivery_add = {
                        "id": sub_uuid,
                        "branch_id": sub_card.card_delivery_address.scb_branch.id,
                        "province_id": None,
                        "district_id": None,
                        "ward_id": None,
                        "card_delivery_address_address": None,
                        "card_delivery_address_note": None,
                    }
                    list_sub_delivery_address.append(sub_delivery_add)
                else:  # neu scb_delivery_address_flag la False thi dia chi nhan la dia chi khac
                    sub_delivery_add = {
                        "id": sub_uuid,
                        "branch_id": None,
                        "province_id": sub_card.card_delivery_address.delivery_address.province.id,
                        "district_id": sub_card.card_delivery_address.delivery_address.district.id,
                        "ward_id": sub_card.card_delivery_address.delivery_address.ward.id,
                        "card_delivery_address_address": sub_card.card_delivery_address.delivery_address.number_and_street,
                        "card_delivery_address_note": sub_card.card_delivery_address.note,
                    }
                    list_sub_delivery_address.append(sub_delivery_add)

                # thong tin (the phu)

                # lưu thông tin card_num_mask thẻ phụ sử dụng để get mã thẻ
                list_primary_card = []
                if sub_card.cif_number:
                    gw_list_sub_card_select_credit_cards_by_cif = await CtrGWCardWorks().ctr_gw_select_credit_cards_by_cif(
                        cif_num=sub_card.cif_number, channel=GW_DEFAULT_SUB_CARD_CHANEL)
                    list_primary_card = gw_list_sub_card_select_credit_cards_by_cif.get("data", {}).get("card_info_list")
                sub_card_num_mask = None

                if list_primary_card:
                    for card in list_primary_card:
                        # todo hard GW_CARD_IS_SUB_CARD GW_CARD_STATUS_IN_USE
                        if card["card_info_item"][
                            "card_is_primary_card"].lower() == GW_CARD_IS_SUB_CARD.lower() and \
                                card["card_info_item"]["card_status"].lower() == GW_CARD_STATUS_IN_USE.lower():
                            sub_card_num_mask = card["card_info_item"]["card_num_mask"]

                sub_data_debit_card = {
                    "id": generate_uuid(),
                    "customer_id": None,
                    "cif_number": sub_card.cif_number,
                    "card_issuance_type_id": sub_card.card_issuance_type.id,
                    "customer_type_id": debt_card_req.issue_debit_card.customer_type.id,
                    "brand_of_card_id": debt_card_req.issue_debit_card.branch_of_card.id,
                    "card_issuance_fee_id": debt_card_req.issue_debit_card.issuance_fee.id,
                    "card_annual_fee_id": debt_card_req.issue_debit_card.annual_fee.id,
                    "src_code": debt_card_req.issue_debit_card.src_code,
                    "pro_code": debt_card_req.issue_debit_card.pro_code,
                    "card_group": debt_card_req.issue_debit_card.card_group,
                    "card_delivery_address_id": sub_uuid,
                    "parent_card_id": id_primary_card,
                    "card_registration_flag": debt_card_req.issue_debit_card.register_flag,
                    "payment_online_flag": sub_card.payment_online_flag,
                    "first_name_on_card": first_name.upper(),  # uppercase first name
                    "last_name_on_card": last_name.upper(),  # uppercase last name
                    "card_delivery_address_flag": sub_card.card_delivery_address.delivery_address_flag,
                    "created_at": now(),
                    "active_flag": 1,
                    "card_num_mask": sub_card_num_mask
                }
                if sub_card.name_on_card.middle_name_on_card:
                    sub_data_debit_card.update({
                        "middle_name_on_card": sub_card.name_on_card.middle_name_on_card.upper()
                    })
                list_sub_debit_card.append(sub_data_debit_card)
                # loai the (the phu)
                for card_type in sub_card.physical_card_type:
                    data_sub_debit_card_type = {
                        "card_id": sub_data_debit_card["id"],
                        "card_type_id": card_type.id,
                    }
                    list_sub_debit_card_type.append(data_sub_debit_card_type)

        """ Insert data thẻ chính """
        uuid = generate_uuid()
        # Địa chỉ nhận thẻ chính
        # neu scb_delivery_address_flag la False thi dia chi nhan la SCB
        if not debt_card_req.card_delivery_address.delivery_address_flag:
            data_card_delivery_address = {
                "id": uuid,
                "branch_id": debt_card_req.card_delivery_address.scb_branch.id,
                "province_id": None,
                "district_id": None,
                "ward_id": None,
                "card_delivery_address_address": None,
                "card_delivery_address_note": None,
            }
        else:  # neu scb_delivery_address_flag la True thi dia chi nhan la dia chi khac
            data_card_delivery_address = {
                "id": uuid,
                "branch_id": None,
                "province_id": debt_card_req.card_delivery_address.delivery_address.province.id,
                "district_id": debt_card_req.card_delivery_address.delivery_address.district.id,
                "ward_id": debt_card_req.card_delivery_address.delivery_address.ward.id,
                "card_delivery_address_address": debt_card_req.card_delivery_address.delivery_address.number_and_street,
                "card_delivery_address_note": debt_card_req.card_delivery_address.note,
            }
        # thong tin the chinh
        session: Session = self.oracle_session
        main_card_cif_num_list = session.execute(select(Customer.cif_number).filter(
            Customer.id == cif_id
        )).scalars().all()
        if len(main_card_cif_num_list) != 1:
            return self.response_exception(
                msg=len(main_card_cif_num_list),
                loc="ctr_debit_card -> main_card_cif_num_list",
                detail="Customer.cif_number must be 1"
            )
        # lưu thông tin thẻ chính dựa vào cif_id thẻ chính gọi qua gw để dùng cho mở thẻ phụ

        gw_list_select_credit_cards_by_cif = await CtrGWCardWorks().ctr_gw_select_credit_cards_by_cif(
            cif_num=main_card_cif_num_list[0], channel=GW_DEFAULT_SUB_CARD_CHANEL)
        list_primary_card = gw_list_select_credit_cards_by_cif.get("data", {}).get("card_info_list")

        card_active_date = None
        card_expire_date = None
        card_status = None
        card_account_num = None
        card_num_mask = None
        card_branch_issue = None
        casa_account_num = None

        if list_primary_card:
            for card in list_primary_card:
                # todo hard GW_CARD_IS_PRIMARY_CARD GW_CARD_STATUS_IN_USE
                if card["card_info_item"]["card_is_primary_card"].lower() == GW_CARD_IS_PRIMARY_CARD.lower() and \
                        card["card_info_item"]["card_status"].lower() == GW_CARD_STATUS_IN_USE.lower():
                    card_active_date = card["card_info_item"]["card_active_date"]
                    card_expire_date = card["card_info_item"]["card_expire_date"]
                    card_status = card["card_info_item"]["card_status"]
                    card_account_num = card["card_info_item"]["card_account_num"]
                    card_num_mask = card["card_info_item"]["card_num_mask"]
                    card_branch_issue = card["card_info_item"]["card_branch_issue"]
                    casa_account_num = card["card_info_item"]["casa_account_num"]

        data_debit_card = {
            "id": id_primary_card,
            "customer_id": cif_id,
            "card_issuance_type_id": debt_card_req.issue_debit_card.physical_issuance_type.id,
            "customer_type_id": debt_card_req.issue_debit_card.customer_type.id,
            "brand_of_card_id": debt_card_req.issue_debit_card.branch_of_card.id,
            "card_issuance_fee_id": debt_card_req.issue_debit_card.issuance_fee.id,
            "card_annual_fee_id": debt_card_req.issue_debit_card.annual_fee.id,
            "src_code": debt_card_req.issue_debit_card.src_code,
            "pro_code": debt_card_req.issue_debit_card.pro_code,
            "card_group": debt_card_req.issue_debit_card.card_group,
            "card_delivery_address_id": uuid,
            "parent_card_id": None,
            "card_registration_flag": debt_card_req.issue_debit_card.register_flag,
            "payment_online_flag": debt_card_req.issue_debit_card.payment_online_flag,
            "first_name_on_card": first_name.upper(),  # uppercase first name
            "last_name_on_card": last_name.upper(),  # uppercase last name
            "card_delivery_address_flag": debt_card_req.card_delivery_address.delivery_address_flag,
            "created_at": now(),
            "active_flag": 1,
            # lưu thông tin thẻ chính dựa vào cif_id thẻ chính gọi qua gw để dùng cho mở thẻ phụ
            "card_active_date": card_active_date,
            "card_expire_date": card_expire_date,
            "card_status": card_status,
            "card_account_num": card_account_num,
            "card_num_mask": card_num_mask,
            "card_branch_issue": card_branch_issue,
            "casa_account_num": casa_account_num
        }
        if debt_card_req.information_debit_card.name_on_card.middle_name_on_card:
            data_debit_card.update({
                "middle_name_on_card": debt_card_req.information_debit_card.name_on_card.middle_name_on_card.upper()
            })

        # loai the (the chinh)
        list_debit_card_type = []
        for debit_card_type_data in debt_card_req.issue_debit_card.physical_card_type:
            debit_card_type = {
                "card_id": data_debit_card["id"],
                "card_type_id": debit_card_type_data.id,
            }
            list_debit_card_type.append(debit_card_type)

        history_datas = self.make_history_log_data(
            description=PROFILE_HISTORY_DESCRIPTIONS_INIT_DEBIT_CARD,
            history_status=PROFILE_HISTORY_STATUS_INIT,
            current_user=current_user
        )

        # Validate history data
        is_success, history_response = validate_history_data(history_datas)
        if not is_success:
            return self.response_exception(
                msg=history_response['msg'],
                loc=history_response['loc'],
                detail=history_response['detail']
            )

        add_debit_card = self.call_repos(
            await repos_add_debit_card(
                cif_id,
                list_sub_card_ids=list_sub_card_ids,
                list_card_type=list_card_type,
                list_delivery_address_ids=list_delivery_address_ids,
                main_card_id=main_card_id,
                data_card_delivery_address=data_card_delivery_address,
                data_debit_card=data_debit_card,
                list_debit_card_type=list_debit_card_type,
                list_sub_delivery_address=list_sub_delivery_address,
                list_sub_debit_card=list_sub_debit_card,
                list_sub_debit_card_type=list_sub_debit_card_type,
                log_data=debt_card_req.json(),
                history_datas=orjson_dumps(history_datas),
                session=self.oracle_session,
            )
        )

        # Lấy Booking Code
        booking = self.call_repos(await repos_get_booking(
            cif_id=cif_id, session=self.oracle_session
        ))
        add_debit_card.update(booking=dict(
            id=booking.id,
            code=booking.code
        ))

        return self.response(data=add_debit_card)
