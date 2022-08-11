ACCOUNT_ALLOW_NUMBER_LENGTH = [0, 8, 10, 11, 12, 16]

CASA_ACCOUNT_STATUS_APPROVED = 1
CASA_ACCOUNT_STATUS_UNAPPROVED = 0

CASA_METHOD_SIGN_ALL = 1
CASA_METHOD_SIGN_ONE = 2
CASA_METHOD_SIGN_PARTLY = 3

RECEIVING_METHOD_SCB_TO_ACCOUNT = 'SCB_TO_ACCOUNT'
RECEIVING_METHOD_SCB_BY_IDENTITY = 'SCB_BY_IDENTITY'
RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT = 'THIRD_PARTY_TO_ACCOUNT'
RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY = 'THIRD_PARTY_BY_IDENTITY'
RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT = 'THIRD_PARTY_247_TO_ACCOUNT'
RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD = 'THIRD_PARTY_247_TO_CARD'

RECEIVING_METHODS = {
    RECEIVING_METHOD_SCB_TO_ACCOUNT: "Trong SCB đến tài khoản",
    RECEIVING_METHOD_SCB_BY_IDENTITY: "Trong SCB nhận bằng giấy tờ định danh",
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT: "Ngoài SCB đến tài khoản",
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY: "Ngoài SCB nhận bằng giấy tờ định danh",
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT: "Ngoài SCB 24/7 tài khoản",
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD: "Ngoài SCB 24/7 số thẻ"
}

RECEIVING_METHOD_SCB = "Trong hệ thống"
RECEIVING_METHOD_THIRD_PARTY = "Ngoài hệ thống"
RECEIVING_METHOD__METHOD_TYPES = {
    RECEIVING_METHOD_SCB_TO_ACCOUNT: RECEIVING_METHOD_SCB,
    RECEIVING_METHOD_SCB_BY_IDENTITY: RECEIVING_METHOD_SCB,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT: RECEIVING_METHOD_THIRD_PARTY,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY: RECEIVING_METHOD_THIRD_PARTY,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT: RECEIVING_METHOD_THIRD_PARTY,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_CARD: RECEIVING_METHOD_THIRD_PARTY
}

RECEIVING_METHOD_IDENTITY_CASES = [
    RECEIVING_METHOD_SCB_BY_IDENTITY,
    RECEIVING_METHOD_THIRD_PARTY_BY_IDENTITY
]

RECEIVING_METHOD_ACCOUNT_CASES = [
    RECEIVING_METHOD_SCB_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_TO_ACCOUNT,
    RECEIVING_METHOD_THIRD_PARTY_247_BY_ACCOUNT
]

PAYER_TRANSFER = 'TRANSFER'
PAYER_RECEIVER = 'RECEIVER'
PAYMENT_PAYERS = {
    PAYER_TRANSFER: "Bên chuyển",
    PAYER_RECEIVER: "Bên nhận"
}


CASA_TOP_UP_NUMBER_TYPE_CASA_ACCOUNT_NUMBER = 'CASA_ACCOUNT_NUMBER'
CASA_TOP_UP_NUMBER_TYPE_IDENTITY_NUMBER = 'IDENTITY_NUMBER'

CASA_TRANSFER_NUMBER_TYPE_CASA_ACCOUNT_NUMBER = 'CASA_ACCOUNT_NUMBER'
CASA_TRANSFER_NUMBER_TYPE_IDENTITY_NUMBER = 'IDENTITY_NUMBER'

CASA_FEE_METHOD_CASH = 'CASH'
CASA_FEE_METHOD_CASA = 'CASA'
CASA_FEE_METHODS = {
    CASA_FEE_METHOD_CASH: 'Thu phí bằng Tiền mặt',
    CASA_FEE_METHOD_CASA: 'Thu phí bằng TKTT'
}
