CIF_STAGE_BEGIN = "CIF_BEGIN"
CIF_STAGE_INIT = "KHOI_TAO_HO_SO"
CIF_STAGE_APPROVE_KSV = "PHE_DUYET_KSV"
CIF_STAGE_APPROVE_KSS = "PHE_DUYET_KSS"
CIF_STAGE_COMPLETED = "KET_THUC_HO_SO"

CIF_ACTION_PHE_DUYET_KSS = "PHE_DUYET_KSS"
CIF_ACTION_BSTTKXTL_KSS = "BSTTKXTL_KSS"
CIF_ACTION_BSTTXTL_KSS = "BSTTXTL_KSS"
CIF_ACTION_XTL_KSS = "XTL_KSS"

CIF_ACTION_PHE_DUYET_KSV = "PHE_DUYET_KSV"
CIF_ACTION_BSTTKXTL_KSV = "BSTTKXTL_KSV"
CIF_ACTION_BSTTXTL_KSV = "BSTTXTL_KSV"
CIF_ACTION_XTL_KSV = "XTL_KSV"

CIF_ACTIONS = {
    CIF_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    CIF_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    CIF_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    CIF_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    CIF_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    CIF_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    CIF_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    CIF_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

CIF_APPROVE_STAGES = {
    CIF_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    CIF_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}

BUSINESS_JOB_CODE_INIT = "OPEN_CIF"
BUSINESS_JOB_CODE_CIF_INFO = "TT_CIF"
BUSINESS_JOB_CODE_CASA_INFO = "TK_TT"
BUSINESS_JOB_CODE_E_BANKING = "E_BANKING"
BUSINESS_JOB_CODE_DEBIT_CARD = "DEBIT_CARD"
BUSINESS_JOB_CODE_SMS_CASA = "SMS_CASA"

BUSINESS_JOB_CODE_START_CASA = "BAT_DAU_CASA"
BUSINESS_JOB_CODE_OPEN_CASA = "MO_TAI_KHOAN"

INIT_RESPONSE = {'status': None, 'error_code': None, 'error_description': None}
FIRST_ITEM = 0

OPEN_CASA_STAGE_BEGIN = 'OPEN_CASA_BEGIN'
OPEN_CASA_STAGE_INIT = "OPEN_CASA_KHOI_TAO_HO_SO"
OPEN_CASA_STAGE_APPROVE_KSV = "OPEN_CASA_PHE_DUYET_KSV"
OPEN_CASA_STAGE_APPROVE_KSS = "OPEN_CASA_PHE_DUYET_KSS"
OPEN_CASA_STAGE_COMPLETED = "OPEN_CASA_KET_THUC_HO_SO"

OPEN_CASA_ACTION_PHE_DUYET_KSS = "OPEN_CASA_PHE_DUYET_KSS"
OPEN_CASA_ACTION_BSTTKXTL_KSS = "OPEN_CASA_BSTTKXTL_KSS"
OPEN_CASA_ACTION_BSTTXTL_KSS = "OPEN_CASA_BSTTXTL_KSS"
OPEN_CASA_ACTION_XTL_KSS = "OPEN_CASA_XTL_KSS"

OPEN_CASA_ACTION_PHE_DUYET_KSV = "OPEN_CASA_PHE_DUYET_KSV"
OPEN_CASA_ACTION_BSTTKXTL_KSV = "OPEN_CASA_BSTTKXTL_KSV"
OPEN_CASA_ACTION_BSTTXTL_KSV = "OPEN_CASA_BSTTXTL_KSV"
OPEN_CASA_ACTION_XTL_KSV = "OPEN_CASA_XTL_KSV"

OPEN_CASA_ACTIONS = {
    OPEN_CASA_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    OPEN_CASA_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    OPEN_CASA_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    OPEN_CASA_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    OPEN_CASA_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    OPEN_CASA_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    OPEN_CASA_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    OPEN_CASA_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

OPEN_CASA_APPROVE_STAGES = {
    OPEN_CASA_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    OPEN_CASA_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}
########################################################################################################################
# AMOUNT_BLOCK
########################################################################################################################
BUSINESS_JOB_CODE_AMOUNT_BLOCK = "PHONG_TOA_TAI_KHOAN"
BUSINESS_JOB_CODE_START_AMOUNT_BLOCK = "BAT_DAT_PHONG_TOA_TAI_KHOAN"

AMOUNT_BLOCK_STAGE_BEGIN = 'AMOUNT_BLOCK_BEGIN'
AMOUNT_BLOCK_STAGE_INIT = "AMOUNT_BLOCK_KHOI_TAO_HO_SO"
AMOUNT_BLOCK_STAGE_APPROVE_KSV = "AMOUNT_BLOCK_PHE_DUYET_KSV"
AMOUNT_BLOCK_STAGE_APPROVE_KSS = "AMOUNT_BLOCK_PHE_DUYET_KSS"
AMOUNT_BLOCK_STAGE_COMPLETED = "AMOUNT_BLOCK_KET_THUC_HO_SO"

AMOUNT_BLOCK_ACTION_PHE_DUYET_KSS = "AMOUNT_BLOCK_PHE_DUYET_KSS"
AMOUNT_BLOCK_ACTION_BSTTKXTL_KSS = "AMOUNT_BLOCK_BSTTKXTL_KSS"
AMOUNT_BLOCK_ACTION_BSTTXTL_KSS = "AMOUNT_BLOCK_BSTTXTL_KSS"
AMOUNT_BLOCK_ACTION_XTL_KSS = "AMOUNT_BLOCK_XTL_KSS"

AMOUNT_BLOCK_ACTION_PHE_DUYET_KSV = "AMOUNT_BLOCK_PHE_DUYET_KSV"
AMOUNT_BLOCK_ACTION_BSTTKXTL_KSV = "AMOUNT_BLOCK_BSTTKXTL_KSV"
AMOUNT_BLOCK_ACTION_BSTTXTL_KSV = "AMOUNT_BLOCK_BSTTXTL_KSV"
AMOUNT_BLOCK_ACTION_XTL_KSV = "AMOUNT_BLOCK_XTL_KSV"

AMOUNT_BLOCK_ACTIONS = {
    AMOUNT_BLOCK_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    AMOUNT_BLOCK_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    AMOUNT_BLOCK_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    AMOUNT_BLOCK_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    AMOUNT_BLOCK_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    AMOUNT_BLOCK_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    AMOUNT_BLOCK_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    AMOUNT_BLOCK_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

AMOUNT_BLOCK_APPROVE_STAGES = {
    AMOUNT_BLOCK_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    AMOUNT_BLOCK_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}
########################################################################################################################
# AMOUNT_UNBLOCK
########################################################################################################################
BUSINESS_JOB_CODE_AMOUNT_UNBLOCK = "GIAI_TOA_TAI_KHOAN"
BUSINESS_JOB_CODE_START_AMOUNT_UNBLOCK = "BAT_DAT_GIAI_TOA_TAI_KHOAN"

AMOUNT_UNBLOCK_STAGE_BEGIN = 'AMOUNT_UNBLOCK_BEGIN'
AMOUNT_UNBLOCK_STAGE_INIT = "AMOUNT_UNBLOCK_KHOI_TAO_HO_SO"
AMOUNT_UNBLOCK_STAGE_APPROVE_KSV = "AMOUNT_UNBLOCK_PHE_DUYET_KSV"
AMOUNT_UNBLOCK_STAGE_APPROVE_KSS = "AMOUNT_UNBLOCK_PHE_DUYET_KSS"
AMOUNT_UNBLOCK_STAGE_COMPLETED = "AMOUNT_UNBLOCK_KET_THUC_HO_SO"

AMOUNT_UNBLOCK_ACTION_PHE_DUYET_KSS = "AMOUNT_UNBLOCK_PHE_DUYET_KSS"
AMOUNT_UNBLOCK_ACTION_BSTTKXTL_KSS = "AMOUNT_UNBLOCK_BSTTKXTL_KSS"
AMOUNT_UNBLOCK_ACTION_BSTTXTL_KSS = "AMOUNT_UNBLOCK_BSTTXTL_KSS"
AMOUNT_UNBLOCK_ACTION_XTL_KSS = "AMOUNT_UNBLOCK_XTL_KSS"

AMOUNT_UNBLOCK_ACTION_PHE_DUYET_KSV = "AMOUNT_UNBLOCK_PHE_DUYET_KSV"
AMOUNT_UNBLOCK_ACTION_BSTTKXTL_KSV = "AMOUNT_UNBLOCK_BSTTKXTL_KSV"
AMOUNT_UNBLOCK_ACTION_BSTTXTL_KSV = "AMOUNT_UNBLOCK_BSTTXTL_KSV"
AMOUNT_UNBLOCK_ACTION_XTL_KSV = "AMOUNT_UNBLOCK_XTL_KSV"

AMOUNT_UNBLOCK_ACTIONS = {
    AMOUNT_UNBLOCK_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    AMOUNT_UNBLOCK_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    AMOUNT_UNBLOCK_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    AMOUNT_UNBLOCK_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    AMOUNT_UNBLOCK_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    AMOUNT_UNBLOCK_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    AMOUNT_UNBLOCK_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    AMOUNT_UNBLOCK_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

AMOUNT_UNBLOCK_APPROVE_STAGES = {
    AMOUNT_UNBLOCK_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    AMOUNT_UNBLOCK_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}

########################################################################################################################
# WITHDRAW
########################################################################################################################
BUSINESS_JOB_CODE_WITHDRAW = "WITHDRAW"

########################################################################################################################
# CLOSE_CASA
########################################################################################################################
BUSINESS_JOB_CODE_CLOSE_CASA = "DONG_TAI_KHOAN"
BUSINESS_JOB_CODE_START_CLOSE_CASA = "BAT_DAT_DONG_TAI_KHOAN"

CLOSE_CASA_STAGE_BEGIN = 'CLOSE_CASA_BEGIN'
CLOSE_CASA_STAGE_INIT = "CLOSE_CASA_KHOI_TAO_HO_SO"
CLOSE_CASA_STAGE_APPROVE_KSV = "CLOSE_CASA_PHE_DUYET_KSV"
CLOSE_CASA_STAGE_APPROVE_KSS = "CLOSE_CASA_PHE_DUYET_KSS"
CLOSE_CASA_STAGE_COMPLETED = "CLOSE_CASA_KET_THUC_HO_SO"

CLOSE_CASA_ACTION_PHE_DUYET_KSS = "CLOSE_CASA_PHE_DUYET_KSS"
CLOSE_CASA_ACTION_BSTTKXTL_KSS = "CLOSE_CASA_BSTTKXTL_KSS"
CLOSE_CASA_ACTION_BSTTXTL_KSS = "CLOSE_CASA_BSTTXTL_KSS"
CLOSE_CASA_ACTION_XTL_KSS = "CLOSE_CASA_XTL_KSS"

CLOSE_CASA_ACTION_PHE_DUYET_KSV = "CLOSE_CASA_PHE_DUYET_KSV"
CLOSE_CASA_ACTION_BSTTKXTL_KSV = "CLOSE_CASA_BSTTKXTL_KSV"
CLOSE_CASA_ACTION_BSTTXTL_KSV = "CLOSE_CASA_BSTTXTL_KSV"
CLOSE_CASA_ACTION_XTL_KSV = "CLOSE_CASA_XTL_KSV"

CLOSE_CASA_ACTIONS = {
    CLOSE_CASA_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    CLOSE_CASA_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    CLOSE_CASA_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    CLOSE_CASA_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    CLOSE_CASA_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    CLOSE_CASA_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    CLOSE_CASA_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    CLOSE_CASA_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

CLOSE_CASA_APPROVE_STAGES = {
    CLOSE_CASA_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    CLOSE_CASA_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}
########################################################################################################################
# OPEN_TD_ACCOUNT
########################################################################################################################
BUSINESS_JOB_CODE_OPEN_TD_ACCOUNT = "MO_TAI_KHOAN_TIET_KIEM"
BUSINESS_JOB_CODE_START_OPEN_TD_ACCOUNT = "BAT_DAT_MO_TAI_KHOAN_TIET_KIEM"

OPEN_TD_ACCOUNT_STAGE_BEGIN = 'OPEN_TD_ACCOUNT_BEGIN'
OPEN_TD_ACCOUNT_STAGE_INIT = "OPEN_TD_ACCOUNT_KHOI_TAO_HO_SO"
OPEN_TD_ACCOUNT_STAGE_APPROVE_KSV = "OPEN_TD_ACCOUNT_PHE_DUYET_KSV"
OPEN_TD_ACCOUNT_STAGE_APPROVE_KSS = "OPEN_TD_ACCOUNT_PHE_DUYET_KSS"
OPEN_TD_ACCOUNT_STAGE_COMPLETED = "OPEN_TD_ACCOUNT_KET_THUC_HO_SO"

OPEN_TD_ACCOUNT_ACTION_PHE_DUYET_KSS = "OPEN_TD_ACCOUNT_PHE_DUYET_KSS"
OPEN_TD_ACCOUNT_ACTION_BSTTKXTL_KSS = "OPEN_TD_ACCOUNT_BSTTKXTL_KSS"
OPEN_TD_ACCOUNT_ACTION_BSTTXTL_KSS = "OPEN_TD_ACCOUNT_BSTTXTL_KSS"
OPEN_TD_ACCOUNT_ACTION_XTL_KSS = "OPEN_TD_ACCOUNT_XTL_KSS"

OPEN_TD_ACCOUNT_ACTION_PHE_DUYET_KSV = "OPEN_TD_ACCOUNT_PHE_DUYET_KSV"
OPEN_TD_ACCOUNT_ACTION_BSTTKXTL_KSV = "OPEN_TD_ACCOUNT_BSTTKXTL_KSV"
OPEN_TD_ACCOUNT_ACTION_BSTTXTL_KSV = "OPEN_TD_ACCOUNT_BSTTXTL_KSV"
OPEN_TD_ACCOUNT_ACTION_XTL_KSV = "OPEN_TD_ACCOUNT_XTL_KSV"

OPEN_TD_ACCOUNT_ACTIONS = {
    OPEN_TD_ACCOUNT_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    OPEN_TD_ACCOUNT_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    OPEN_TD_ACCOUNT_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    OPEN_TD_ACCOUNT_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    OPEN_TD_ACCOUNT_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    OPEN_TD_ACCOUNT_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    OPEN_TD_ACCOUNT_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    OPEN_TD_ACCOUNT_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

OPEN_TD_ACCOUNT_APPROVE_STAGES = {
    OPEN_TD_ACCOUNT_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    OPEN_TD_ACCOUNT_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}

########################################################################################################################


########################################################################################################################
# CASA_TOP_UP
########################################################################################################################
BUSINESS_JOB_CODE_START_CASA_TOP_UP = "CASA_TOP_UP_BAT_DAU"
BUSINESS_JOB_CODE_CASA_TOP_UP = "CASA_TOP_UP_KHOI_TAO"

CASA_TOP_UP_STAGE_BEGIN = 'CASA_TOP_UP_BEGIN'
CASA_TOP_UP_STAGE_INIT = "CASA_TOP_UP_KHOI_TAO_HO_SO"
CASA_TOP_UP_STAGE_APPROVE_KSV = "CASA_TOP_UP_PHE_DUYET_KSV"
CASA_TOP_UP_STAGE_APPROVE_KSS = "CASA_TOP_UP_PHE_DUYET_KSS"
CASA_TOP_UP_STAGE_COMPLETED = "CASA_TOP_UP_KET_THUC_HO_SO"

CASA_TOP_UP_ACTION_PHE_DUYET_KSS = "CASA_TOP_UP_PHE_DUYET_KSS"
CASA_TOP_UP_ACTION_BSTTKXTL_KSS = "CASA_TOP_UP_BSTTKXTL_KSS"
CASA_TOP_UP_ACTION_BSTTXTL_KSS = "CASA_TOP_UP_BSTTXTL_KSS"
CASA_TOP_UP_ACTION_XTL_KSS = "CASA_TOP_UP_XTL_KSS"

CASA_TOP_UP_ACTION_PHE_DUYET_KSV = "CASA_TOP_UP_PHE_DUYET_KSV"
CASA_TOP_UP_ACTION_BSTTKXTL_KSV = "CASA_TOP_UP_BSTTKXTL_KSV"
CASA_TOP_UP_ACTION_BSTTXTL_KSV = "CASA_TOP_UP_BSTTXTL_KSV"
CASA_TOP_UP_ACTION_XTL_KSV = "CASA_TOP_UP_XTL_KSV"

CASA_TOP_UP_ACTIONS = {
    CASA_TOP_UP_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    CASA_TOP_UP_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    CASA_TOP_UP_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    CASA_TOP_UP_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    CASA_TOP_UP_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    CASA_TOP_UP_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    CASA_TOP_UP_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    CASA_TOP_UP_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

CASA_TOP_UP_APPROVE_STAGES = {
    CASA_TOP_UP_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    CASA_TOP_UP_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}
########################################################################################################################

########################################################################################################################
# CASA_TRANSFER
########################################################################################################################
BUSINESS_JOB_CODE_START_CASA_TRANSFER = "TRANSFER_BAT_DAU"
BUSINESS_JOB_CODE_CASA_TRANSFER = "TRANSFER_KHOI_TAO"

CASA_TRANSFER_STAGE_BEGIN = 'TRANSFER_BEGIN'
CASA_TRANSFER_STAGE_INIT = "TRANSFER_KHOI_TAO_HO_SO"
CASA_TRANSFER_STAGE_APPROVE_KSV = "TRANSFER_PHE_DUYET_KSV"
CASA_TRANSFER_STAGE_APPROVE_KSS = "TRANSFER_PHE_DUYET_KSS"
CASA_TRANSFER_STAGE_COMPLETED = "TRANSFER_KET_THUC_HO_SO"

CASA_TRANSFER_ACTION_PHE_DUYET_KSS = "TRANSFER_PHE_DUYET_KSS"
CASA_TRANSFER_ACTION_BSTTKXTL_KSS = "TRANSFER_BSTTKXTL_KSS"
CASA_TRANSFER_ACTION_BSTTXTL_KSS = "TRANSFER_BSTTXTL_KSS"
CASA_TRANSFER_ACTION_XTL_KSS = "TRANSFER_XTL_KSS"

CASA_TRANSFER_ACTION_PHE_DUYET_KSV = "TRANSFER_PHE_DUYET_KSV"
CASA_TRANSFER_ACTION_BSTTKXTL_KSV = "TRANSFER_BSTTKXTL_KSV"
CASA_TRANSFER_ACTION_BSTTXTL_KSV = "TRANSFER_BSTTXTL_KSV"
CASA_TRANSFER_ACTION_XTL_KSV = "TRANSFER_XTL_KSV"

CASA_TRANSFER_ACTIONS = {
    CASA_TRANSFER_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    CASA_TRANSFER_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    CASA_TRANSFER_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    CASA_TRANSFER_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    CASA_TRANSFER_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    CASA_TRANSFER_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    CASA_TRANSFER_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    CASA_TRANSFER_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

CASA_TRANSFER_APPROVE_STAGES = {
    CASA_TRANSFER_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    CASA_TRANSFER_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}

########################################################################################################################

########################################################################################################################
# CASA_WITHDRAW
########################################################################################################################
BUSINESS_JOB_CODE_START_CASA_WITHDRAW = "WITHDRAW_BAT_DAU"
BUSINESS_JOB_CODE_CASA_WITHDRAW = "WITHDRAW_KHOI_TAO"

CASA_WITHDRAW_STAGE_BEGIN = 'WITHDRAW_BEGIN'
CASA_WITHDRAW_STAGE_INIT = "WITHDRAW_KHOI_TAO_HO_SO"
CASA_WITHDRAW_STAGE_APPROVE_KSV = "WITHDRAW_PHE_DUYET_KSV"
CASA_WITHDRAW_STAGE_APPROVE_KSS = "WITHDRAW_PHE_DUYET_KSS"
CASA_WITHDRAW_STAGE_COMPLETED = "WITHDRAW_KET_THUC_HO_SO"

CASA_WITHDRAW_ACTION_PHE_DUYET_KSS = "WITHDRAW_PHE_DUYET_KSS"
CASA_WITHDRAW_ACTION_BSTTKXTL_KSS = "WITHDRAW_BSTTKXTL_KSS"
CASA_WITHDRAW_ACTION_BSTTXTL_KSS = "WITHDRAW_BSTTXTL_KSS"
CASA_WITHDRAW_ACTION_XTL_KSS = "WITHDRAW_XTL_KSS"

CASA_WITHDRAW_ACTION_PHE_DUYET_KSV = "WITHDRAW_PHE_DUYET_KSV"
CASA_WITHDRAW_ACTION_BSTTKXTL_KSV = "WITHDRAW_BSTTKXTL_KSV"
CASA_WITHDRAW_ACTION_BSTTXTL_KSV = "WITHDRAW_BSTTXTL_KSV"
CASA_WITHDRAW_ACTION_XTL_KSV = "WITHDRAW_XTL_KSV"

CASA_WITHDRAW_ACTIONS = {
    CASA_WITHDRAW_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    CASA_WITHDRAW_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    CASA_WITHDRAW_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    CASA_WITHDRAW_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    CASA_WITHDRAW_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    CASA_WITHDRAW_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    CASA_WITHDRAW_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    CASA_WITHDRAW_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

CASA_WITHDRAW_APPROVE_STAGES = {
    CASA_WITHDRAW_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    CASA_WITHDRAW_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}

########################################################################################################################


STAGE_BEGINS = [
    CIF_STAGE_BEGIN,
    OPEN_CASA_STAGE_BEGIN,
    AMOUNT_BLOCK_STAGE_BEGIN,
    AMOUNT_UNBLOCK_STAGE_BEGIN,
    CLOSE_CASA_STAGE_BEGIN,
    OPEN_TD_ACCOUNT_STAGE_BEGIN,
    CASA_TOP_UP_STAGE_BEGIN,
    CASA_WITHDRAW_STAGE_BEGIN,
    CASA_TRANSFER_STAGE_BEGIN,
]

INIT_STAGES = [
    CIF_STAGE_INIT,
    OPEN_CASA_STAGE_INIT,
    CLOSE_CASA_STAGE_INIT,
    OPEN_TD_ACCOUNT_STAGE_INIT,
    AMOUNT_BLOCK_STAGE_INIT,
    AMOUNT_UNBLOCK_STAGE_INIT,
    CASA_TOP_UP_STAGE_INIT,
    CASA_WITHDRAW_STAGE_INIT,
    CASA_TRANSFER_STAGE_INIT,
]

APPROVE_SUPERVISOR_STAGES = [
    CIF_STAGE_APPROVE_KSV,
    OPEN_CASA_STAGE_APPROVE_KSV,
    CLOSE_CASA_STAGE_APPROVE_KSV,
    OPEN_TD_ACCOUNT_STAGE_APPROVE_KSV,
    AMOUNT_BLOCK_STAGE_APPROVE_KSV,
    AMOUNT_UNBLOCK_STAGE_APPROVE_KSV,
    CASA_TOP_UP_STAGE_APPROVE_KSV,
    CASA_WITHDRAW_STAGE_APPROVE_KSV,
    CASA_TRANSFER_STAGE_APPROVE_KSV,
]

APPROVE_AUDIT_STAGES = [
    CIF_STAGE_APPROVE_KSS,
    OPEN_CASA_STAGE_APPROVE_KSS,
    CLOSE_CASA_STAGE_APPROVE_KSS,
    OPEN_TD_ACCOUNT_STAGE_APPROVE_KSS,
    AMOUNT_BLOCK_STAGE_APPROVE_KSS,
    AMOUNT_UNBLOCK_STAGE_APPROVE_KSS,
    CASA_TOP_UP_STAGE_APPROVE_KSS,
    CASA_WITHDRAW_STAGE_APPROVE_KSS,
    CASA_TRANSFER_STAGE_APPROVE_KSS,
]

COMPLETED_STAGES = [
    CIF_STAGE_COMPLETED,
    OPEN_CASA_STAGE_COMPLETED,
    CLOSE_CASA_STAGE_COMPLETED,
    OPEN_TD_ACCOUNT_STAGE_COMPLETED,
    AMOUNT_BLOCK_STAGE_COMPLETED,
    AMOUNT_UNBLOCK_STAGE_COMPLETED,
    CASA_TOP_UP_STAGE_COMPLETED,
    CASA_WITHDRAW_STAGE_COMPLETED,
    CASA_TRANSFER_STAGE_COMPLETED,
]

ROLE_CODE_TELLER = "GDV"
ROLE_CODE_SUPERVISOR = "KSV"
ROLE_CODE_AUDIT = "KSS"

ROLE_CODES = {
    ROLE_CODE_TELLER: "Giao dịch viên",
    ROLE_CODE_SUPERVISOR: "Kiểm soát viên",
    ROLE_CODE_AUDIT: "Kiểm soát sau"
}
