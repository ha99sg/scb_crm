from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingAccount, BookingBusinessForm, BookingCustomer,
    TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    SlaTransaction, TransactionJob, TransactionStage, TransactionStageLane,
    TransactionStagePhase, TransactionStageRole, TransactionStageStatus
)
from app.utils.constant.approval import BUSINESS_JOB_CODE_START_CLOSE_CASA
from app.utils.constant.cif import BUSINESS_FORM_CLOSE_CASA
from app.utils.functions import generate_uuid, now


@auto_commit
async def repos_save_close_casa_account(
        booking_id,
        saving_transaction_stage_status,
        saving_transaction_stage,
        saving_transaction_stage_lane,
        saving_sla_transaction,
        saving_transaction_stage_phase,
        saving_transaction_stage_role,
        saving_transaction_daily,
        saving_transaction_sender,
        saving_booking_account,
        saving_booking_customer,
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
            business_form_id=BUSINESS_FORM_CLOSE_CASA,
            save_flag=True,
            log_data=history_data,
            created_at=now()
        )),
        TransactionJob(**dict(
            transaction_id=generate_uuid(),
            booking_id=booking_id,
            business_job_id=BUSINESS_JOB_CODE_START_CLOSE_CASA,
            complete_flag=True,
            error_code=None,
            error_desc=None,
            created_at=now()
        ))
    ])
    # Update Booking
    session.bulk_save_objects(BookingAccount(**account) for account in saving_booking_account)
    session.bulk_save_objects(BookingCustomer(**customer) for customer in saving_booking_customer)
    session.execute(
        update(Booking)
        .filter(Booking.id == booking_id)
        .values(transaction_id=saving_transaction_daily['transaction_id'])
    )
    session.flush()
    return ReposReturn(data=booking_id)