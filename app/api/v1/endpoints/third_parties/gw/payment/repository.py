from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.others.booking.repository import generate_booking_code
from app.settings.event import service_gw
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm
)
from app.utils.constant.business_type import (
    BUSINESS_TYPE_AMOUNT_BLOCK, BUSINESS_TYPE_AMOUNT_UNBLOCK
)
from app.utils.constant.gw import GW_CASA_RESPONSE_STATUS_SUCCESS
from app.utils.error_messages import ERROR_BOOKING_CODE_EXISTED, MESSAGE_STATUS
from app.utils.functions import generate_uuid, now, orjson_dumps


@auto_commit
async def repos_create_booking_payment(
        business_type_code: str,
        current_user,
        form_data,
        log_data,
        session: Session
):
    booking_id = generate_uuid()
    current_user_branch_code = current_user.hrm_branch_code
    is_existed, booking_code = await generate_booking_code(
        branch_code=current_user_branch_code,
        business_type_code=business_type_code,
        session=session
    )
    if is_existed:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BOOKING_CODE_EXISTED + f", booking_code: {booking_code}",
            detail=MESSAGE_STATUS[ERROR_BOOKING_CODE_EXISTED]
        )

    session.add_all([
        Booking(
            id=booking_id,
            # TODO hard core transaction
            transaction_id=None,
            code=booking_code,
            business_type_id=business_type_code,
            branch_id=current_user_branch_code,
            created_at=now(),
            updated_at=now()
        ),
        BookingBusinessForm(
            booking_id=booking_id,
            business_form_id=business_type_code,
            save_flag=False,
            form_data=orjson_dumps(form_data),
            log_data=orjson_dumps(log_data),
            created_at=now()
        )
    ])
    return ReposReturn(data=(booking_id, booking_code))


async def repos_gw_payment_amount_block(
    current_user,
    data_input,
    session
):
    is_success, gw_payment_amount_block = await service_gw.gw_payment_amount_block(
        current_user=current_user.user_info, data_input=data_input
    )
    booking = await repos_create_booking_payment(
        business_type_code=BUSINESS_TYPE_AMOUNT_BLOCK,
        current_user=current_user.user_info,
        form_data=data_input,
        log_data=gw_payment_amount_block,
        session=session
    )
    booking_id, booking_code = booking.data

    amount_block_out = gw_payment_amount_block.get('amountBlock_out', {})

    # check trường hợp lỗi
    if amount_block_out.get('transaction_info').get('transaction_error_code') != GW_CASA_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=amount_block_out.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=(booking_id, gw_payment_amount_block))


async def repos_gw_payment_amount_unblock(current_user, data_input, session):
    is_success, gw_payment_amount_unblock = await service_gw.gw_payment_amount_unblock(
        data_input=data_input,
        current_user=current_user.user_info
    )

    booking = await repos_create_booking_payment(
        business_type_code=BUSINESS_TYPE_AMOUNT_UNBLOCK,
        current_user=current_user.user_info,
        form_data=data_input,
        log_data=gw_payment_amount_unblock,
        session=session
    )
    booking_id, booking_code = booking.data

    amount_unblock_out = gw_payment_amount_unblock.get('amountUnBlock_out', {})

    # check trường hợp lỗi
    if amount_unblock_out.get('transaction_info').get('transaction_error_code') != GW_CASA_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=amount_unblock_out.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=(booking_id, gw_payment_amount_unblock))


async def repos_gw_pay_in_cash(current_user, data_input):
    is_success, gw_pay_in_cash = await service_gw.gw_payment_amount_unblock(
        data_input=data_input,
        current_user=current_user.user_info
    )
    pay_in_cash = gw_pay_in_cash.get('amountUnBlock_out', {})

    # check trường hợp lỗi
    if pay_in_cash.get('transaction_info').get('transaction_error_code') != GW_CASA_RESPONSE_STATUS_SUCCESS:
        return ReposReturn(is_error=True, msg=pay_in_cash.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=gw_pay_in_cash)
