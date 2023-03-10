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


@auto_commit
async def repos_save_close_casa_account(
        booking_id: str,
        saving_transaction_stage_status: dict,
        saving_sla_transaction: dict,
        saving_transaction_stage: dict,
        saving_transaction_stage_phase: dict,
        saving_transaction_stage_lane: dict,
        saving_transaction_stage_role: dict,
        saving_transaction_daily: dict,
        saving_transaction_sender: dict,
        saving_transaction_job: dict,
        saving_booking_business_form: dict,
        saving_booking_account,
        saving_booking_customer,
        session: Session
) -> ReposReturn:

    session.add_all([
        TransactionStageStatus(**saving_transaction_stage_status),
        SlaTransaction(**saving_sla_transaction),
        TransactionStage(**saving_transaction_stage),
        TransactionStageLane(**saving_transaction_stage_lane),
        TransactionStagePhase(**saving_transaction_stage_phase),
        TransactionStageRole(**saving_transaction_stage_role),
        TransactionDaily(**saving_transaction_daily),
        TransactionSender(**saving_transaction_sender),
        TransactionJob(**saving_transaction_job),
        BookingBusinessForm(**saving_booking_business_form)

        # lưu form data request từ client
        # BookingBusinessForm(**dict(
        #     booking_id=booking_id,
        #     form_data=request_json,
        #     business_form_id=BUSINESS_FORM_CLOSE_CASA,
        #     save_flag=True,
        #     log_data=history_data,
        #     created_at=now()
        # )),
        # TransactionJob(**dict(
        #     transaction_id=generate_uuid(),
        #     booking_id=booking_id,
        #     business_job_id=BUSINESS_JOB_CODE_START_CLOSE_CASA,
        #     complete_flag=True,
        #     error_code=None,
        #     error_desc=None,
        #     created_at=now()
        # ))
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
