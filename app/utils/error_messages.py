# status error
from app.utils.constant.approval import CIF_APPROVE_STAGES
from app.utils.constant.casa import (
    ACCOUNT_ALLOW_NUMBER_LENGTH, CASA_FEE_METHODS, PAYMENT_PAYERS,
    RECEIVING_METHODS
)

PAGING_ERROR = "PAGING_ERROR"
VALIDATE_ERROR = "VALIDATE_ERROR"

USER_ID_NOT_EXIST = "USER_ID_NOT_EXIST"
USER_CODE_NOT_EXIST = "USER_CODE_NOT_EXIST"
USER_NOT_EXIST = "USER_NOT_EXIST"
USERNAME_OR_PASSWORD_INVALID = "USERNAME_OR_PASSWORD_INVALID"
ERROR_INVALID_TOKEN = "INVALID_TOKEN"
ERROR_INVALID_TOKEN_CHANGE_DEVICE = "ERROR_INVALID_TOKEN_CHANGE_DEVICE"

ERROR_CALL_SERVICE_FILE = "ERROR_CALL_SERVICE_FILE"
ERROR_CALL_SERVICE_EKYC = "ERROR_CALL_SERVICE_EKYC"
ERROR_CALL_SERVICE_TEMPLATE = "ERROR_CALL_SERVICE_TEMPLATE"
ERROR_CALL_SERVICE_DWH = "ERROR_CALL_SERVICE_DWH"
ERROR_CALL_SERVICE_IDM = "ERROR_CALL_SERVICE_IDM"
ERROR_CALL_SERVICE_GW = 'ERROR_CALL_SERVICE_GW'
ERROR_NO_INSTRUMENT_NUMBER = 'ERROR_NO_INSTRUMENT_NUMBER'
INVALID_TRANSACTION_FORM = 'INVALID TRANSACTION FORM'
ERROR_CUSTOMER_DETAIL_CALL_SERVICE_SOA = "ERROR_CUSTOMER_DETAIL_CALL_SERVICE_SOA"

ERROR_FILE_IS_NULL = "ERROR_FILE_IS_NULL"
ERROR_FILE_TOO_LARGE = "ERROR_FILE_TOO_LARGE"
ERROR_TOO_MANY_FILE = "ERROR_TOO_MANY_FILE"

ERROR_ID_NOT_EXIST = "ID_NOT_EXIST"
ERROR_IDS_NOT_EXIST = "ID_NOT_EXIST"
ERROR_COMMENT_DOES_NOT_EXITS = "COMMENT_DOES_NOT_EXIST"

ERROR_COMMIT = "ERROR_COMMIT"

ERROR_CIF_ID_NOT_EXIST = "CIF_ID_NOT_EXIST"
ERROR_CIF_NUMBER_DUPLICATED = "CIF_NUMBER_DUPLICATED"
ERROR_CIF_NUMBER_EXIST = "CIF_NUMBER_EXIST"
ERROR_CIF_NUMBER_NOT_EXIST = "CIF_NUMBER_NOT_EXIST"
ERROR_CIF_NUMBER_NOT_EXIST_IN_CRM = "ERROR_CIF_NUMBER_NOT_EXIST_IN_CRM"
ERROR_CIF_NUMBER_INVALID = "ERROR_CIF_NUMBER_INVALID"
ERROR_CIF_NUMBER_MORE_THAN_ONE = "CIF_NUMBER_MORE_THAN_ONE"

ERROR_CIF_NUMBER_NOT_DUPLICATE = "CIF_NUMBER_NOT_DUPLICATE"
ERROR_CIF_NUMBER_NOT_EXIST_IN_CO_OWNER = "CIF_NUMBER_NOT_EXIST_IN_CO_OWNER"
ERROR_CIF_NUMBER_NOT_COMPLETED = "CIF_NUMBER_NOT_COMPLETED"

ERROR_CUSTOMER_NOT_EXIST = "ERROR_CUSTOMER_NOT_EXIST"

ERROR_GUARDIAN_INFO_DOES_NOT_EXITS = "ERROR_GUARDIAN_INFO_DOES_NOT_EXITS"
ERROR_IDENTITY_DOCUMENT_NOT_EXIST = "ERROR_IDENTITY_DOCUMENT_NOT_EXIST"
ERROR_SUB_IDENTITY_DOCUMENT_NOT_EXIST = "ERROR_SUB_IDENTITY_DOCUMENT_NOT_EXIST"
ERROR_DOCUMENT_ID_DOES_NOT_EXIST = "ERROR_DOCUMENT_ID_DOES_NOT_EXIST"
ERROR_ACCOUNT_ID_DOES_NOT_EXIST = "ERROR_ACCOUNT_ID_DOES_NOT_EXIST_IN_JOINT_ACC_AGREE"
ERROR_CASA_ACCOUNT_NOT_EXIST = "CASA_ACCOUNT_NOT_EXIST"
ERROR_CASA_BALANCE_UNAVAILABLE = "CASA_BALANCE_UNAVAILABLE"
ERROR_AMOUNT_INVALID = "ERROR_AMOUNT_INVALID"
ERROR_CASA_ACCOUNT_ID_DOES_NOT_EXIST = "ERROR_CASA_ACCOUNT_ID_DOES_NOT_EXIST"
ERROR_CASA_ACCOUNT_DOES_NOT_HAVE_ENOUGH_MONEY = "ERROR_CASA_ACCOUNT_DOES_NOT_HAVE_ENOUGH_MONEY"
ERROR_BOOKING_PARENT_DOES_NOT_EXIST = "ERROR_BOOKING_PARENT_DOES_NOT_EXIST"
ERROR_CASA_FILE_ID_DOES_NOT_EXIST = "ERROR_CASA_FILE_ID_DOES_NOT_EXIST"
ERROR_DOCUMENT_NO_DOES_NOT_EXIST = "ERROR_DOCUMENT_NO_DOES_NOT_EXIST"
ERROR_CASA_ACCOUNT_ID_DOES_NOT_EXIST_IN_JOINT_ACCOUNT_AGREEMENT = \
    "ERROR_CASA_ACCOUNT_ID_DOES_NOT_EXIST_IN_JOINT_ACCOUNT_HOLDER_AGREEMENT"
ERROR_CASA_ACCOUNT_EXIST = "CASA_ACCOUNT_EXIST"
ERROR_ACCOUNT_NUM_EXIST = "ACCOUNT_NUM_EXIST"
ERROR_CASA_ACCOUNT_APPROVED = "ERROR_CASA_ACCOUNT_APPROVED"
ERROR_CUSTOMER_INDIVIDUAL_INFO = "CUSTOMER_INDIVIDUAL_INFO_NOT_EXIST"
ERROR_CUSTOMER_IDENTITY = "CUSTOMER_IDENTITY_NOT_EXIST"
ERROR_CUSTOMER_IDENTITY_IMAGE = "CUSTOMER_IDENTITY_IMAGE_NOT_EXIST"
ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST = "AGREEMENT_AUTHORIZATIONS_NOT_EXIST"
ERROR_CAN_NOT_CREATE = "CAN_NOT_CREATE"

ERROR_IMAGE_TYPE_NOT_EXIST = 'IMAGE_TYPE_NOT_EXIST'
ERROR_SIGNATURE_IS_NULL = "ERROR_SIGNATURE_IS_NULL"
ERROR_PHONE_NUMBER = "ERROR_PHONE_NUMBER"
ERROR_PHONE_NUMBER_NOT_EXITS = "PHONE_NUMBER_NOT_EXITS"

ERROR_RELATION_CUSTOMER_SELF_RELATED = "ERROR_CUSTOMER_SELF_RELATED"
ERROR_RELATIONSHIP_EXIST = "ERROR_RELATION_EXIST"
ERROR_RELATIONSHIP_TYPE_ID_NOT_EXIST = "ERROR_RELATIONSHIP_TYPE_ID_NOT_EXIST"
ERROR_RELATIONSHIP_NOT_GUARDIAN = "ERROR_RELATIONSHIP_NOT_GUARDIAN"

ERROR_INVALID_URL = "ERROR_INVALID_URL"
ERROR_INVALID_NUMBER = "ERROR_INVALID_NUMBER"
ERROR_INVALID_TOTAL = "ERROR_INVALID_TOTAL"

ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST = "ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST"
ERROR_WRONG_TYPE_IDENTITY = "ERROR_WRONG_TYPE_IDENTITY"

ERROR_NOT_NULL = "ERROR_NOT_NULL"

ERROR_NO_DATA = "ERROR_NO_DATA"

ERROR_WRONG_STAGE_ACTION = "ERROR_WRONG_STAGE_ACTION"
ERROR_STAGE_TELLER_NOT_EXIST = "ERROR_STAGE_TELLER_NOT_EXIST"
ERROR_BEGIN_STAGE_NOT_EXIST = "ERROR_BEGIN_STAGE_NOT_EXIST"
ERROR_NEXT_STAGE_NOT_EXIST = "ERROR_NEXT_STAGE_NOT_EXIST"
ERROR_NEXT_RECEIVER_NOT_EXIST = "ERROR_NEXT_RECEIVER_NOT_EXIST"
ERROR_STAGE_NOT_EXIST = "ERROR_STAGE_NOT_EXIST"
ERROR_STAGE_COMPLETED = "ERROR_STAGE_COMPLETED"
ERROR_CONTENT_NOT_NULL = "ERROR_CONTENT_NOT_NULL"

ERROR_NOT_REGISTER = "ERROR_NOT_REGISTER"

ERROR_COMPARE_IMAGE_IS_EXISTED = "ERROR_COMPARE_IMAGE_IS_EXISTED"

ERROR_E_BANKING = "ERROR_E-BANKING"

ERROR_MOBILE_NUMBER = "ERROR_MOBILE_NUMBER_NOT_NULL"

ERROR_APPROVAL_UPLOAD_FACE = "ERROR_APPROVAL_UPLOAD_FACE"
ERROR_APPROVAL_INCORRECT_UPLOAD_FACE = "ERROR_APPROVAL_INCORRECT_UPLOAD_FACE"
ERROR_APPROVAL_UPLOAD_FINGERPRINT = "ERROR_APPROVAL_UPLOAD_FINGERPRINT"
ERROR_APPROVAL_INCORRECT_UPLOAD_FINGERPRINT = "ERROR_APPROVAL_INCORRECT_UPLOAD_FINGERPRINT"
ERROR_APPROVAL_UPLOAD_SIGNATURE = "ERROR_APPROVAL_UPLOAD_SIGNATURE"
ERROR_APPROVAL_INCORRECT_UPLOAD_SIGNATURE = "ERROR_APPROVAL_INCORRECT_UPLOAD_SIGNATURE"
ERROR_APPROVAL_NO_DATA_IN_IDENTITY_STEP = "ERROR_APPROVAL_NO_DATA_IN_IDENTITY_STEP"
ERROR_APPROVAL_NO_FACE_IN_IDENTITY_STEP = "ERROR_APPROVAL_NO_FACE_IN_IDENTITY_STEP"
ERROR_APPROVAL_NO_FINGERPRINT_IN_IDENTITY_STEP = "ERROR_APPROVAL_NO_FINGERPRINT_IN_IDENTITY_STEP"
ERROR_APPROVAL_NO_SIGNATURE_IN_IDENTITY_STEP = "ERROR_APPROVAL_NO_SIGNATURE_IN_IDENTITY_STEP"
ERROR_APPROVAL_STAGE_NOT_EXISTED = "ERROR_APPROVAL_STAGE_NOT_EXISTED"

ERROR_VALIDATE = "ERROR_VALIDATE"
ERROR_FIELD_REQUIRED = "ERROR_FIELD_REQUIRED"
ERROR_VALIDATE_ONE_FIELD_REQUIRED = "ERROR_VALIDATE_ONE_FIELD_REQUIRED"
ERROR_GROUP_ROLE_CODE = "GROUP_ROLE_CODE"
ERROR_MENU_CODE = "ERROR_MENU_CODE"
ERROR_PERMISSION = 'ERROR_PERMISSION'
ERROR_BOOKING_CODE_EXISTED = 'ERROR_BOOKING_CODE_EXISTED'
ERROR_BOOKING_ID_NOT_EXIST = 'ERROR_BOOKING_ID_NOT_EXIST'
ERROR_BOOKING_IS_COMPLETED = 'ERROR_BOOKING_IS_COMPLETED'
ERROR_BOOKING_CODE_NOT_EXIST = 'ERROR_BOOKING_CODE_NOT_EXIST'
ERROR_BOOKING_INCORRECT = 'ERROR_BOOKING_INCORRECT'
ERROR_BOOKING_ALREADY_USED = 'ERROR_BOOKING_ALREADY_USED'
ERROR_BOOKING_TRANSACTION_NOT_EXIST = 'ERROR_BOOKING_TRANSACTION_NOT_EXIST'
ERROR_BOOKING_BUSINESS_FORM_NOT_EXIST = 'ERROR_BOOKING_BUSINESS_FORM_NOT_EXIST'

ERROR_BUSINESS_TYPE_NOT_EXIST = 'ERROR_BUSINESS_TYPE_NOT_EXIST'
ERROR_BUSINESS_TYPE_CODE_INCORRECT = 'ERROR_BUSINESS_TYPE_CODE_INCORRECT'

ERROR_IDENTITY_TYPE_NOT_EXIST = 'ERROR_IDENTITY_TYPE_NOT_EXIST'

ERROR_OPEN_CIF = 'ERROR_OPEN_CIF'

ERROR_SLA_TRANSACTION_NOT_EXIST = 'ERROR_SLA_TRANSACTION_NOT_EXIST'

ERROR_ACCOUNT_NUMBER_NOT_NULL = 'ERROR_ACCOUNT_NUMBER_NOT_NULL'
ERROR_ACCOUNT_LENGTH_NOT_ALLOWED = 'ERROR_ACCOUNT_LENGTH_NOT_ALLOWED'

ERROR_RECEIVING_METHOD_NOT_EXIST = 'ERROR_RECEIVING_METHOD_NOT_EXIST'
ERROR_DENOMINATIONS_NOT_EXIST = 'ERROR_DENOMINATIONS_NOT_EXIST'

ERROR_ISSUED_DATE = 'ERROR_ISSUED_DATE'

ERROR_MAPPING_MODEL = 'ERROR_MAPPING_MODEL'
ERROR_PREVIOUS_STAGE_NOT_EXIST = 'PREVIOUS_STAGE_NOT_EXIST'

ERROR_INTERBANK_ACCOUNT_NUMBER_NOT_EXIST = 'ERROR_INTERBANK_ACCOUNT_NUMBER_NOT_EXIST'
ERROR_INTERBANK_CARD_NUMBER_NOT_EXIST = 'ERROR_INTERBANK_CARD_NUMBER_NOT_EXIST'

ERROR_BANK_NOT_IN_CITAD = 'ERROR_BANK_NOT_IN_CITAD'
ERROR_BANK_NOT_IN_NAPAS = 'ERROR_BANK_NOT_IN_NAPAS'

ERROR_CASA_FEE_METHOD_NOT_EXIST = 'CASA_FEE_METHOD_NOT_EXIST'
ERROR_FEE_ID_NOT_EXIST = 'ERROR_FEE_ID_NOT_EXIST'
ERROR_INPUT_MORE_THAN_ONE_FEE = 'ERROR_INPUT_MORE_THAN_ONE_FEE'

ERROR_CUSTOMER_EKYC_NOT_EXIST = 'ERROR_CUSTOMER_EKYC_NOT_EXIST'
ERROR_CUSTOMER_EKYC_EXIST = 'ERROR_CUSTOMER_EKYC_EXIST'

ERROR_ACCOUNT_CLASS_NOT_EXIST = 'ERROR_ACCOUNT_CLASS_NOT_EXIST'

ERROR_USER_NOT_THE_SAME_BRANCH = 'ERROR_USER_NOT_THE_SAME_BRANCH'

ERROR_PAYER_NOT_EXIST = 'ERROR_PAYER_NOT_EXIST'

ERROR_TABLET_OTP_INVALID = 'ERROR_TABLET_OTP_INVALID'
ERROR_TABLET_IS_NOT_PAIRED = 'ERROR_TABLET_IS_NOT_PAIRED'
ERROR_TABLET_INVALID_TOKEN = "INVALID_TABLET_TOKEN"

ERROR_TEMPLATE_NOT_EXIST = 'ERROR_TEMPLATE_NOT_EXIST'

MESSAGE_STATUS = {
    # general error
    PAGING_ERROR: "Can not found page!",
    VALIDATE_ERROR: "Validate error!",
    ERROR_VALIDATE_ONE_FIELD_REQUIRED: "Validate error! At least one field required!",

    USER_ID_NOT_EXIST: "User id is not exist",
    USER_NOT_EXIST: "User is not exist",
    USERNAME_OR_PASSWORD_INVALID: "Username or password is invalid",
    ERROR_INVALID_TOKEN: "Token is invalid",
    ERROR_INVALID_TOKEN_CHANGE_DEVICE: "Token has been changed",

    ERROR_CALL_SERVICE_FILE: "Call service file error",
    ERROR_CALL_SERVICE_EKYC: "Call service eKYC error",
    ERROR_CALL_SERVICE_TEMPLATE: "Call service template error",
    ERROR_CALL_SERVICE_DWH: "Call service DWH error",
    ERROR_CUSTOMER_DETAIL_CALL_SERVICE_SOA: "Customer detail call service SOA error",
    ERROR_FILE_IS_NULL: "File can not be empty",
    ERROR_FILE_TOO_LARGE: "File size is too large",
    ERROR_TOO_MANY_FILE: "Upload too many file",

    ERROR_COMMIT: "Commit to database error",

    ERROR_ID_NOT_EXIST: "Id is not exist",
    ERROR_IDS_NOT_EXIST: "Ids is not exist",
    ERROR_CIF_NUMBER_EXIST: "CIF number is exist",
    ERROR_CIF_NUMBER_NOT_EXIST: "CIF number does not exist",
    ERROR_CIF_NUMBER_NOT_EXIST_IN_CRM: "CIF number does not exist in CRM",
    ERROR_CIF_NUMBER_DUPLICATED: "CIF numbers are duplicated",
    ERROR_CIF_NUMBER_INVALID: "CIF number must be number",
    ERROR_CIF_NUMBER_NOT_COMPLETED: "CIF number have not completed",

    ERROR_CIF_ID_NOT_EXIST: "CIF id is not exist",

    ERROR_CUSTOMER_NOT_EXIST: "Customer is not exist",

    ERROR_IDENTITY_DOCUMENT_NOT_EXIST: "Identity Document is not exist",
    ERROR_SUB_IDENTITY_DOCUMENT_NOT_EXIST: 'Sub Identity is not exist',
    ERROR_CAN_NOT_CREATE: 'Can not create',
    ERROR_IMAGE_TYPE_NOT_EXIST: 'Image type is not exist',
    ERROR_SIGNATURE_IS_NULL: "Signature can not be empty",
    ERROR_PHONE_NUMBER: "Phone number only 9 to 10 numbers and start with 0",

    ERROR_RELATIONSHIP_TYPE_ID_NOT_EXIST: "Relationship type does not exist",
    ERROR_RELATION_CUSTOMER_SELF_RELATED: "Customer can not relate to himself/herself",
    ERROR_RELATIONSHIP_EXIST: "guardian/customer relationship existed",
    ERROR_RELATIONSHIP_NOT_GUARDIAN: "Can not be guardian, because cif_number has guardian(s)",
    ERROR_CASA_ACCOUNT_NOT_EXIST: "casa_account not exist",
    ERROR_CASA_ACCOUNT_EXIST: "casa_account is existed",
    ERROR_CASA_ACCOUNT_APPROVED: "Casa Account is approved",
    ERROR_CUSTOMER_INDIVIDUAL_INFO: "customer_individual_info is not exist",
    ERROR_CUSTOMER_IDENTITY: "customer_identity is not exist",
    ERROR_CUSTOMER_IDENTITY_IMAGE: "customer_identity_image is not exist",
    ERROR_AGREEMENT_AUTHORIZATIONS_NOT_EXIST: "agreement_authorizations is not exist",

    ERROR_INVALID_URL: "url is invalid",
    ERROR_INVALID_NUMBER: "number is invalid",
    ERROR_INVALID_TOTAL: "total is invalid",

    ERROR_IDENTITY_DOCUMENT_TYPE_TYPE_NOT_EXIST: "Identity Document Type Type is not exist",
    ERROR_WRONG_TYPE_IDENTITY: "Identity Document Type Type is wrong",

    ERROR_NOT_NULL: " field is not null",

    ERROR_NO_DATA: "No data, please create data before get data",

    ERROR_WRONG_STAGE_ACTION: "Action is wrong, please insert correct action",
    ERROR_STAGE_TELLER_NOT_EXIST: "Stage Teller is not existed",
    ERROR_BEGIN_STAGE_NOT_EXIST: "Begin Stage is not existed",
    ERROR_NEXT_STAGE_NOT_EXIST: "Next Stage is not existed",
    ERROR_NEXT_RECEIVER_NOT_EXIST: "Next Receiver is not existed",
    ERROR_STAGE_NOT_EXIST: "Stage is not existed",
    ERROR_STAGE_COMPLETED: "Stage completed",
    ERROR_CONTENT_NOT_NULL: "Content is not null",

    ERROR_COMPARE_IMAGE_IS_EXISTED: "Compare Image is existed, please upload new compare image",
    ERROR_NOT_REGISTER: "No debit card registration",

    ERROR_APPROVAL_UPLOAD_FACE: "Face is not upload, please upload face before submit",
    ERROR_APPROVAL_INCORRECT_UPLOAD_FACE: "Upload face is incorrect",
    ERROR_APPROVAL_UPLOAD_FINGERPRINT: "Fingerprint is not upload, please upload fingerprint before submit",
    ERROR_APPROVAL_INCORRECT_UPLOAD_FINGERPRINT: "Upload fingerprint is incorrect",
    ERROR_APPROVAL_UPLOAD_SIGNATURE: "Signature is not upload, please upload signature before submit",
    ERROR_APPROVAL_INCORRECT_UPLOAD_SIGNATURE: "Upload signature is incorrect",
    ERROR_APPROVAL_NO_DATA_IN_IDENTITY_STEP: "No Data in Identity Step",
    ERROR_APPROVAL_NO_FACE_IN_IDENTITY_STEP: "No Face in Identity Step",
    ERROR_APPROVAL_NO_FINGERPRINT_IN_IDENTITY_STEP: "No Fingerprint in Identity Step",
    ERROR_APPROVAL_NO_SIGNATURE_IN_IDENTITY_STEP: "No Signature in Identity Step",
    ERROR_APPROVAL_STAGE_NOT_EXISTED: f"Stage Code must be in {CIF_APPROVE_STAGES} or None",
    ERROR_VALIDATE: "Validate error",
    ERROR_FIELD_REQUIRED: 'Field required',
    ERROR_GROUP_ROLE_CODE: "Group_role_code is not exist",
    ERROR_MENU_CODE: "Menu_code is not exist",
    ERROR_PERMISSION: "Permission Denied",

    ERROR_BOOKING_CODE_EXISTED: "Booking code is existed",
    ERROR_BOOKING_CODE_NOT_EXIST: "Booking code not exist",
    ERROR_BOOKING_ID_NOT_EXIST: "Booking ID not exist",
    ERROR_BOOKING_IS_COMPLETED: "Booking is completed",
    ERROR_BOOKING_INCORRECT: "Booking is incorrect",
    ERROR_BOOKING_ALREADY_USED: "Booking already used",
    ERROR_BOOKING_TRANSACTION_NOT_EXIST: "Booking transaction not exist",
    ERROR_BOOKING_BUSINESS_FORM_NOT_EXIST: "Booking business form not exist",

    ERROR_BUSINESS_TYPE_NOT_EXIST: "Business type not exist",
    ERROR_BUSINESS_TYPE_CODE_INCORRECT: "Business type code incorrect",

    ERROR_IDENTITY_TYPE_NOT_EXIST: "Identity type not exist",

    ERROR_OPEN_CIF: "Cannot open CIF",

    ERROR_SLA_TRANSACTION_NOT_EXIST: "SLA Transaction not exist",
    ERROR_NO_INSTRUMENT_NUMBER: "No instrument number",

    ERROR_ACCOUNT_NUMBER_NOT_NULL: 'Account number is not null',
    ERROR_ACCOUNT_LENGTH_NOT_ALLOWED: f'Account number length must be in range {ACCOUNT_ALLOW_NUMBER_LENGTH}',

    ERROR_RECEIVING_METHOD_NOT_EXIST: f'Receiving method not in {RECEIVING_METHODS}',

    ERROR_ISSUED_DATE: 'Issue date must be lower than today',

    ERROR_MAPPING_MODEL: 'Mapping model is wrong',

    ERROR_PREVIOUS_STAGE_NOT_EXIST: 'Previous Stage not exist',
    ERROR_INTERBANK_ACCOUNT_NUMBER_NOT_EXIST: 'Interbank account number not exist',
    ERROR_INTERBANK_CARD_NUMBER_NOT_EXIST: 'Interbank card number not exist',

    ERROR_BANK_NOT_IN_CITAD: 'Bank not in citad',
    ERROR_BANK_NOT_IN_NAPAS: 'Bank not in napas',

    ERROR_CASA_FEE_METHOD_NOT_EXIST: f'CASA fee method must be in {CASA_FEE_METHODS}',
    ERROR_FEE_ID_NOT_EXIST: 'Fee id not exist',

    ERROR_CUSTOMER_EKYC_NOT_EXIST: "Customer EKYC not exist",
    ERROR_CUSTOMER_EKYC_EXIST: "Customer EKYC existed",

    ERROR_ACCOUNT_CLASS_NOT_EXIST: "Account Class not exist",
    ERROR_USER_NOT_THE_SAME_BRANCH: "User not the same branch",

    ERROR_PAYER_NOT_EXIST: f"Payer not exist in {PAYMENT_PAYERS}",

    ERROR_TABLET_OTP_INVALID: "OTP for tablet is invalid",
    ERROR_TABLET_IS_NOT_PAIRED: "You are not connected to the tablet",
    ERROR_TABLET_INVALID_TOKEN: "Invalid tablet token",

    ERROR_TEMPLATE_NOT_EXIST: "template does not exist"
}

ERROR_EMAIL_TEMPLATES_GW = 'ERROR_EMAIL_TEMPLATES_GW'
