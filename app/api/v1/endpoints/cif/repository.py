import re
from typing import List

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.settings.event import service_soa
from app.third_parties.oracle.models.cif.basic_information.contact.model import (
    CustomerAddress
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.cif.basic_information.personal.model import (
    CustomerIndividualInfo
)
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingBusinessForm, BookingCustomer, TransactionDaily,
    TransactionSender
)
from app.third_parties.oracle.models.master_data.address import AddressCountry
from app.third_parties.oracle.models.master_data.customer import (
    CustomerClassification, CustomerEconomicProfession, CustomerGender,
    CustomerStatus, CustomerType
)
from app.third_parties.oracle.models.master_data.identity import PlaceOfIssue
from app.third_parties.oracle.models.master_data.others import (
    KYCLevel, MaritalStatus
)
from app.utils.error_messages import (
    ERROR_BOOKING_CODE_NOT_EXIST, ERROR_CALL_SERVICE_SOA,
    ERROR_CIF_ID_NOT_EXIST, ERROR_CIF_NUMBER_EXIST, ERROR_CIF_NUMBER_INVALID,
    ERROR_CIF_NUMBER_NOT_EXIST, MESSAGE_STATUS
)
from app.utils.functions import dropdown


async def repos_get_initializing_customer(cif_id: str, session: Session) -> ReposReturn:
    customer = session.execute(
        select(
            Customer
        ).filter(
            Customer.id == cif_id,
            Customer.complete_flag == 0
        )
    ).scalar()
    if not customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=customer)


async def repos_get_cif_info(cif_id: str, session: Session) -> ReposReturn:
    customer_info = session.execute(
        select(
            Customer.cif_number,
            Customer.self_selected_cif_flag,
            CustomerClassification,
            CustomerEconomicProfession,
            KYCLevel
        )
        .join(CustomerClassification, Customer.customer_classification_id == CustomerClassification.id)
        .join(CustomerEconomicProfession, Customer.customer_economic_profession_id == CustomerEconomicProfession.id)
        .join(KYCLevel, Customer.kyc_level_id == KYCLevel.id)
        .filter(
            Customer.id == cif_id,
            Customer.active_flag == 1
        )
    ).first()
    if not customer_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_ID_NOT_EXIST,
            loc='cif_id'
        )
    cif_number, self_selected_cif_flag, customer_classification, customer_economic_profession, kyc_level = customer_info
    return ReposReturn(data={
        "self_selected_cif_flag": self_selected_cif_flag,
        "cif_number": cif_number,
        "customer_classification": dropdown(customer_classification),
        "customer_economic_profession": dropdown(customer_economic_profession),
        "kyc_level": dropdown(kyc_level)
    })


async def repos_profile_history(cif_id: str, session: Session) -> ReposReturn:
    histories = session.execute(
        select(
            BookingCustomer,
            Booking,
            BookingBusinessForm
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(BookingBusinessForm, Booking.id == BookingBusinessForm.booking_id)
        .filter(
            BookingCustomer.customer_id == cif_id
        )
    ).all()

    # if not histories:
    #     return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc='cif_id')

    return ReposReturn(data=histories)


async def repos_customer_information(cif_id: str, session: Session) -> ReposReturn:
    query_data_customer = session.execute(
        select(
            Customer,
            CustomerIdentity,
            CustomerIndividualInfo,
            CustomerAddress,
            CustomerStatus,
            PlaceOfIssue,
            AddressCountry,
            CustomerClassification,
            CustomerGender,
            MaritalStatus,
            CustomerType
        )
        .join(CustomerIdentity, Customer.id == CustomerIdentity.customer_id)
        .join(CustomerIndividualInfo, Customer.id == CustomerIndividualInfo.customer_id)
        .join(CustomerStatus, Customer.customer_status_id == CustomerStatus.id)
        .join(CustomerAddress, Customer.id == CustomerAddress.customer_id)
        .join(PlaceOfIssue, CustomerIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(AddressCountry, CustomerIndividualInfo.country_of_birth_id == AddressCountry.id)
        .join(CustomerClassification, Customer.customer_classification_id == CustomerClassification.id)
        .join(CustomerGender, CustomerIndividualInfo.gender_id == CustomerGender.id)
        .outerjoin(MaritalStatus, CustomerIndividualInfo.marital_status_id == MaritalStatus.id)
        .outerjoin(CustomerType, Customer.customer_type_id == CustomerType.id)
        .filter(
            Customer.id == cif_id
        ).order_by(desc(CustomerIdentity.maker_at))
    ).all()

    if not query_data_customer:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")

    return ReposReturn(data=query_data_customer)


async def repos_get_customer_identity(cif_id: str, session: Session):
    identity = session.execute(
        select(
            CustomerIdentity
        ).filter(CustomerIdentity.customer_id == cif_id).order_by(desc(CustomerIdentity.maker_at))
    ).scalars().first()

    if not identity:
        return ReposReturn(is_error=True, msg=ERROR_CIF_ID_NOT_EXIST, loc="cif_id")
    return ReposReturn(data=identity)


async def repos_check_not_exist_cif_number(cif_number: str, session: Session) -> ReposReturn:
    # TODO: call to core
    cif_number = session.execute(
        select(
            Customer.cif_number
        ).filter(Customer.cif_number == cif_number)
    ).scalars().first()

    if cif_number:
        return ReposReturn(is_error=True, msg=ERROR_CIF_NUMBER_EXIST, loc="cif_number")

    return ReposReturn(data='Cif number is not exist')


async def repos_get_customers_by_cif_numbers(
        cif_numbers: List[str],
        session: Session
) -> ReposReturn:
    customers = session.execute(
        select(
            Customer
        ).filter(
            Customer.cif_number.in_(cif_numbers),
            Customer.complete_flag == 1
        )
    ).scalars().all()
    if not customers or len(cif_numbers) != len(customers):
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_NUMBER_NOT_EXIST,
            loc="cif_number"
        )

    return ReposReturn(data=customers)


async def repos_check_exist_cif(cif_number: str):
    is_success, customer_detail = await service_soa.retrieve_customer_ref_data_mgmt(cif_number=cif_number)
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_SOA, detail=customer_detail["message"])

    return ReposReturn(data={
        "is_existed": customer_detail["is_existed"]
    })


async def repos_validate_cif_number(cif_number: str):
    regex = re.search("[0-9]+", cif_number)
    if not regex or len(regex.group()) != len(cif_number):
        return ReposReturn(
            is_error=True,
            msg=ERROR_CIF_NUMBER_INVALID,
            detail=f"{MESSAGE_STATUS[ERROR_CIF_NUMBER_INVALID]}: cif_number={cif_number}",
            loc="cif_number"
        )
    return ReposReturn(data=None)


async def repos_retrieve_customer_information_by_cif_number(
        cif_number: str,
        # flat_address: bool
):
    is_success, customer_information = await service_soa.retrieve_customer_information_by_cif_number(
        cif_number=cif_number,
        # flat_address=flat_address
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=ERROR_CALL_SERVICE_SOA, detail=customer_information["message"])

    return ReposReturn(data=customer_information)


async def repos_get_total_participants(
    cif_id: str,
    session: Session
):
    transaction_root_id = session.execute(
        select(
            TransactionDaily.transaction_root_id,
            BookingCustomer,
            Booking
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .filter(BookingCustomer.customer_id == cif_id)
    ).scalar()

    total_participants = session.execute(
        select(
            TransactionSender.user_id,
            TransactionSender.user_fullname,
            TransactionSender.user_name,
            TransactionSender.user_email,
            TransactionSender.position_id,
            TransactionSender.position_code,
            TransactionSender.position_name,
            TransactionSender.department_id,
            TransactionSender.department_code,
            TransactionSender.department_name,
            TransactionSender.branch_id,
            TransactionSender.branch_code,
            TransactionSender.branch_name,
            TransactionDaily.transaction_root_id
        )
        .join(TransactionSender, TransactionDaily.transaction_id == TransactionSender.transaction_id)
        .filter(TransactionDaily.transaction_root_id == transaction_root_id)
        .distinct()
    ).all()
    return ReposReturn(data=total_participants)


async def repos_get_booking_code(
    cif_id: str,
    session: Session
):
    booking_code = session.execute(
        select(
            Booking.code,
            BookingCustomer
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .filter(BookingCustomer.customer_id == cif_id)
    ).scalar()
    if not booking_code:
        return ReposReturn(is_error=True, msg=ERROR_BOOKING_CODE_NOT_EXIST)
    return ReposReturn(data=booking_code)
