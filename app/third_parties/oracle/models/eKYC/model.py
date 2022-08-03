from sqlalchemy import CLOB, VARCHAR, Column, DateTime, text, DATE
from sqlalchemy.dialects.oracle import NUMBER

from app.third_parties.oracle.base import Base


class EKYCCustomer(Base):
    __tablename__ = 'crm_ekyc_customer'

    id = Column(NUMBER, primary_key=True)
    customer_id = Column(VARCHAR(100), nullable=False)
    document_id = Column(VARCHAR(12), nullable=True)
    document_type = Column(NUMBER(2), nullable=True)
    date_of_issue = Column(DATE, nullable=True)
    place_of_issue = Column(VARCHAR(1000), nullable=True)
    qr_code_data = Column(VARCHAR(1000), nullable=True)
    full_name = Column(VARCHAR(1000), nullable=True)
    date_of_birth = Column(DATE, nullable=True)
    gender = Column(VARCHAR(1), nullable=True)
    place_of_residence = Column(VARCHAR(1000), nullable=True)
    place_of_origin = Column(VARCHAR(1000), nullable=True)
    nationality = Column(VARCHAR(500), nullable=True)
    address_1 = Column(VARCHAR(1000), nullable=True)
    address_2 = Column(VARCHAR(1000), nullable=True)
    address_3 = Column(VARCHAR(1000), nullable=True)
    address_4 = Column(VARCHAR(1000), nullable=True)
    phone_number = Column(VARCHAR(12), nullable=True)
    ocr_data = Column(CLOB, nullable=True)
    extra_info = Column(CLOB, nullable=True)
    receive_ads = Column(NUMBER(1), nullable=True)
    longitude = Column(NUMBER, nullable=True)
    latitude = Column(NUMBER, nullable=True)
    cif = Column('cif', VARCHAR(500), nullable=True)
    account_number = Column(VARCHAR(100), nullable=True)
    ekyc_step_info = Column(CLOB, nullable=True)
    job_title = Column(VARCHAR(100), nullable=True)
    organization = Column(VARCHAR(500), nullable=True)
    organization_address = Column(VARCHAR(1000), nullable=True)
    organization_phone_number = Column(VARCHAR(100), nullable=True)
    position = Column(VARCHAR(500), nullable=True)
    salary_range = Column(VARCHAR(100), nullable=True)
    tax_number = Column(VARCHAR(10), nullable=True)
    created_date = Column(DATE, nullable=True)
    faces_matching_percent = Column(NUMBER, nullable=True)
    ocr_data_errors = Column(CLOB, nullable=True)
    permanent_address = Column(CLOB, nullable=True)
    transaction_id = Column(VARCHAR(100), nullable=False)
    delete_flag = Column(NUMBER(1), nullable=True)
    open_biometric = Column(NUMBER(1), nullable=True)
    date_of_expiry = Column(DATE, nullable=True)
    user_eb = Column(VARCHAR(500), nullable=True)
    transaction_data = Column(CLOB, nullable=False)


class EKYCCustomerStep(Base):
    __tablename__ = 'crm_ekyc_customer_step'
    id = Column(NUMBER, primary_key=True)
    step = Column(VARCHAR(50), nullable=True)
    start_date = Column(DATE, nullable=True)
    end_date = Column(DATE, nullable=True)
    step_status = Column(VARCHAR(100), nullable=True)
    update_at = Column(DATE, nullable=True)
    reason = Column(VARCHAR(500), nullable=True)
    customer_id = Column(VARCHAR(100), nullable=False)
    transaction_id = Column(VARCHAR(100), nullable=False)
