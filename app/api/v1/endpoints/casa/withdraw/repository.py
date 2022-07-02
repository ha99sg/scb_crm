from sqlalchemy import desc, select, update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.cif.payment_account.model import (
    CasaAccount
)
from app.third_parties.oracle.models.master_data.others import (
    SlaTransaction, TransactionJob, TransactionStage, TransactionStageLane,
    TransactionStagePhase, TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.approval import BUSINESS_JOB_CODE_WITHDRAW
from app.utils.constant.cif import BUSINESS_FORM_WITHDRAW
from app.utils.error_messages import ERROR_BOOKING_ID_NOT_EXIST
from app.utils.functions import generate_uuid, now


@auto_commit
async def repos_save_withdraw(
        booking_id,
        saving_transaction_stage_status,
        saving_transaction_stage,
        saving_transaction_stage_lane,
        saving_sla_transaction,
        saving_transaction_stage_phase,
        saving_transaction_stage_role,
        saving_transaction_daily,
        saving_transaction_sender,
        request_json,
        history_data,
        session: Session
) -> ReposReturn:
    session.add_all([
        TransactionStageStatus(**saving_transaction_stage_status),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        SlaTransaction(**saving_sla_transaction),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        # lưu form data request từ client
        BookingBusinessForm(**dict(
            booking_id=booking_id,
            form_data=request_json,
            business_form_id=BUSINESS_FORM_WITHDRAW,
            save_flag=True,
            log_data=history_data,
            created_at=now()
        )),
        TransactionJob(**dict(
            transaction_id=generate_uuid(),
            booking_id=booking_id,
            business_job_id=BUSINESS_JOB_CODE_WITHDRAW,
            complete_flag=True,
            error_code=None,
            error_desc=None,
            created_at=now()
        ))
    ])
    # Update Booking
    session.execute(
        update(Booking)
        .filter(Booking.id == booking_id)
        .values(transaction_id=saving_transaction_daily['transaction_id'])
    )
    session.flush()

    return ReposReturn(data=booking_id)


async def repos_get_withdraw_info(booking_id: str, session: Session):
    get_withdraw_info = session.execute(
        select(
            BookingBusinessForm
        )
        .filter(BookingBusinessForm.booking_id == booking_id)
        .order_by(desc(BookingBusinessForm.created_at))
    ).scalars().first()

    if not get_withdraw_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BOOKING_ID_NOT_EXIST,
            detail='booking_id'
        )

    return ReposReturn(data=get_withdraw_info)


async def repos_get_acc_types(numbers: list, session: Session):
    get_acc_types = session.execute(
        select(
            CasaAccount.casa_account_number,
            CasaAccount.acc_type_id
        ).filter(CasaAccount.casa_account_number.in_(numbers))
    ).all()

    return ReposReturn(data=get_acc_types)
