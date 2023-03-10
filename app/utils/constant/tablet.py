OTP_EXPIRED_AFTER_IN_SECONDS = 2 * 60

MAX_RETRY_GENERATE_NEW_OTP = 5

DEVICE_TYPE_WEB = 'WEB'
DEVICE_TYPE_MOBILE = 'MOBILE'

RABBITMQ_EXCHANGE_AMQ_TOPIC = 'amq.topic'

WEB_ACTION_PAIRED = 'PAIRED'  # server gửi ở API Sync With Web By OTP (nhập mã OTP thành công ở mobile)
WEB_ACTION_FOUND_CUSTOMER = 'FOUND_CUSTOMER'  # server gửi ở API  Enter Identity Number (tìm thấy khách hàng)
WEB_ACTION_NOT_FOUND_CUSTOMER = 'NOT_FOUND_CUSTOMER'  # server gửi ở API  Enter Identity Number (không tìm thấy khách hàng)
WEB_ACTION_RECEIVED_PHOTO = 'RECEIVED_PHOTO'  # server gửi ở API chụp ảnh (không phải chụp để xác thực)


MOBILE_ACTION_UNPAIRED = 'UNPAIRED'  # server gửi ở API Unpair (khi logout hoặc quá 15 phút)
MOBILE_ACTION_ENTER_IDENTITY_NUMBER = 'ENTER_IDENTITY_NUMBER'  # cho FE gửi
MOBILE_ACTION_ENTER_IDENTITY_NUMBER_FAIL = 'ENTER_IDENTITY_NUMBER_FAIL'  # server gửi ở API Enter Identity Number (khi không tìm thấy)
MOBILE_ACTION_TAKE_DOCUMENT_PHOTO = 'TAKE_DOCUMENT_PHOTO'  # cho FE gửi ở thao tác liên quan hoặc cho server gửi khi tìm ra khách hàng ở bước nhập thông tin
MOBILE_ACTION_TAKE_FACE_PHOTO = 'TAKE_FACE_PHOTO'  # cho FE gửi ở thao tác liên quan hoặc cho server gửi khi tìm ra khách hàng ở bước nhập thông tin
MOBILE_ACTION_PROCESS_TRANSACTION = 'PROCESS_TRANSACTION'  # cho FE gửi
MOBILE_ACTION_NEW_TRANSACTION = 'NEW_TRANSACTION'  # cho FE gửi
MOBILE_ACTION_SIGN = 'SIGN'  # cho FE gửi
MOBILE_ACTION_TRANSACT_SUCCESS = 'TRANSACT_SUCCESS'  # cho FE gửi


LIST_BANNER_LANGUAGE_CODE_VIETNAMESE = 'vi'
LIST_BANNER_LANGUAGE_CODE_ENGLISH = 'en'
LIST_BANNER_LANGUAGE_NAME_VIETNAMESE = 'Tiếng Việt'
LIST_BANNER_LANGUAGE_NAME_ENGLISH = 'English'
