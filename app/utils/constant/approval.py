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
BUSINESS_JOB_CODE_DEBIT_CARD = "TGN"

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
# CLOSE_CASA
########################################################################################################################
BUSINESS_JOB_CODE_CLOSE_CASA = "DONG_TAI_KHOAN"
BUSINESS_JOB_CODE_START_CLOSE_CASA = "BAT_DAT_DONG_TAI_KHOAN"

CLOSE_CASA_STAGE_BEGIN = 'CLOSE_CASA_BEGIN'
CLOSE_CASA_STAGE_INIT = "CLOSE_CASA_KHOI_TAO_HO_SO"
CLOSE_CASA_STAGE_APPROVE_KSV = "CLOSE_CASA_PHE_DUYET_KSV"
CLOSE_CASA_STAGE_APPROVE_KSS = "CLOSE_CASA_PHE_DUYET_KSS"
CLOSE_CASA_STAGE_COMPLETED = "CLOSE_CASA_KET_THUC_HO_SO"

WITHDRAW_KHOI_TAO = "WITHDRAW_KHOI_TAO"
WITHDRAW_UNBLOCK_PD = "WITHDRAW_UNBLOCK_PD"

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


########################################################################################################################
# PAY_IN_CASH
########################################################################################################################
BUSINESS_JOB_CODE_PAY_IN_CASH = "PHONG_TOA_TAI_KHOAN"
BUSINESS_JOB_CODE_START_PAY_IN_CASH = "BAT_DAT_PHONG_TOA_TAI_KHOAN"

PAY_IN_CASH_STAGE_BEGIN = 'PAY_IN_CASH_BEGIN'
PAY_IN_CASH_STAGE_INIT = "PAY_IN_CASH_KHOI_TAO_HO_SO"
PAY_IN_CASH_STAGE_APPROVE_KSV = "PAY_IN_CASH_PHE_DUYET_KSV"
PAY_IN_CASH_STAGE_APPROVE_KSS = "PAY_IN_CASH_PHE_DUYET_KSS"
PAY_IN_CASH_STAGE_COMPLETED = "PAY_IN_CASH_KET_THUC_HO_SO"

PAY_IN_CASH_ACTION_PHE_DUYET_KSS = "PAY_IN_CASH_PHE_DUYET_KSS"
PAY_IN_CASH_ACTION_BSTTKXTL_KSS = "PAY_IN_CASH_BSTTKXTL_KSS"
PAY_IN_CASH_ACTION_BSTTXTL_KSS = "PAY_IN_CASH_BSTTXTL_KSS"
PAY_IN_CASH_ACTION_XTL_KSS = "PAY_IN_CASH_XTL_KSS"

PAY_IN_CASH_ACTION_PHE_DUYET_KSV = "PAY_IN_CASH_PHE_DUYET_KSV"
PAY_IN_CASH_ACTION_BSTTKXTL_KSV = "PAY_IN_CASH_BSTTKXTL_KSV"
PAY_IN_CASH_ACTION_BSTTXTL_KSV = "PAY_IN_CASH_BSTTXTL_KSV"
PAY_IN_CASH_ACTION_XTL_KSV = "PAY_IN_CASH_XTL_KSV"

PAY_IN_CASH_ACTIONS = {
    PAY_IN_CASH_ACTION_PHE_DUYET_KSS: "KSS Phê duyệt ",
    PAY_IN_CASH_ACTION_BSTTKXTL_KSS: "KSS Bổ sung thông tin không cần xác thực lại",
    PAY_IN_CASH_ACTION_BSTTXTL_KSS: "KSS Bổ sung thông tin và xác thực lại",
    PAY_IN_CASH_ACTION_XTL_KSS: "KSS Yêu cầu xác thực lại khách hàng.",

    PAY_IN_CASH_ACTION_PHE_DUYET_KSV: "KSV Phê duyệt",
    PAY_IN_CASH_ACTION_BSTTKXTL_KSV: "KSV Bổ sung thông tin không cần xác thực lại",
    PAY_IN_CASH_ACTION_BSTTXTL_KSV: "KSV Bổ sung thông tin và xác thực lại",
    PAY_IN_CASH_ACTION_XTL_KSV: "KSV Yêu cầu xác thực lại khách hàng."
}

PAY_IN_CASH_APPROVE_STAGES = {
    PAY_IN_CASH_STAGE_APPROVE_KSV: "Phê duyệt KSV",
    PAY_IN_CASH_STAGE_APPROVE_KSS: "Phê duyệt KSS"
}
########################################################################################################################

STAGE_BEGINS = [
    CIF_STAGE_BEGIN,
    OPEN_CASA_STAGE_BEGIN,
    AMOUNT_BLOCK_STAGE_BEGIN,
    AMOUNT_UNBLOCK_STAGE_BEGIN,
    CLOSE_CASA_STAGE_BEGIN,
]

INIT_STAGES = [
    CIF_STAGE_INIT,
    OPEN_CASA_STAGE_INIT,
    AMOUNT_BLOCK_STAGE_INIT,
    AMOUNT_UNBLOCK_STAGE_INIT,
    CLOSE_CASA_STAGE_INIT
]

APPROVE_SUPERVISOR_STAGES = [
    CIF_STAGE_APPROVE_KSV,
    OPEN_CASA_STAGE_APPROVE_KSV,
    AMOUNT_BLOCK_STAGE_APPROVE_KSV,
    AMOUNT_UNBLOCK_STAGE_APPROVE_KSV,
    CLOSE_CASA_STAGE_APPROVE_KSV,
]

APPROVE_AUDIT_STAGES = [
    CIF_STAGE_APPROVE_KSS,
    OPEN_CASA_STAGE_APPROVE_KSS,
    AMOUNT_BLOCK_STAGE_APPROVE_KSS,
    AMOUNT_UNBLOCK_STAGE_APPROVE_KSS,
    CLOSE_CASA_STAGE_APPROVE_KSS,
]

COMPLETED_STAGES = [
    CIF_STAGE_COMPLETED,
    OPEN_CASA_STAGE_COMPLETED,
    AMOUNT_BLOCK_STAGE_COMPLETED,
    AMOUNT_UNBLOCK_STAGE_COMPLETED,
    CLOSE_CASA_STAGE_COMPLETED,
]

ROLE_CODE_TELLER = "GDV"
ROLE_CODE_SUPERVISOR = "KSV"
ROLE_CODE_AUDIT = "KSS"

ROLE_CODES = {
    ROLE_CODE_TELLER: "Giao dịch viên",
    ROLE_CODE_SUPERVISOR: "Kiểm soát viên",
    ROLE_CODE_AUDIT: "Kiểm soát sau"
}
