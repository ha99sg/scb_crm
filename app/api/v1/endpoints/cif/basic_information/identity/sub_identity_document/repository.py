import json
from typing import List

from sqlalchemy import and_, delete, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn, auto_commit
from app.api.v1.endpoints.repository import (
    write_transaction_log_and_update_booking
)
from app.third_parties.oracle.models.cif.basic_information.identity.model import (
    CustomerIdentityImage, CustomerIdentityImageTransaction,
    CustomerSubIdentity
)
from app.third_parties.oracle.models.cif.basic_information.model import (
    Customer
)
from app.third_parties.oracle.models.master_data.identity import (
    CustomerSubIdentityType, PlaceOfIssue
)
from app.utils.constant.cif import (
    BUSINESS_FORM_TTCN_GTDD_GTDDP, IMAGE_TYPE_CODE_SUB_IDENTITY
)
from app.utils.error_messages import ERROR_SUB_IDENTITY_DOCUMENT_NOT_EXIST
from app.utils.functions import dropdown

SUB_IDENTITY_INFO = [
    {
        "id": "1",
        "name": "Giấy tờ định danh phụ 1",
        "sub_identity_document_type": {
            "id": "1",
            "code": "THETAMTRU",
            "name": "Thẻ tạm trú"
        },
        "sub_identity_document_image_url": "http://example.com/example.jpg",
        "ocr_result": {
            "sub_identity_number": "361963424",
            "symbol": "LĐ",
            "full_name_vn": "Nguyễn Văn A",
            "date_of_birth": "1990-08-12",
            "province": {
                "id": "2",
                "code": "HN",
                "name": "Hà Nội"
            },
            "place_of_issue": {
                "id": "2",
                "code": "HCDS",
                "name": "Cục hành chính về trật tự xã hội"
            },
            "expired_date": "2021-02-07",
            "issued_date": "2021-02-07"
        }
    }
]
SUB_IDENTITY_LOGS_INFO = [
    {
        "reference_flag": True,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "1",
            "code": "THETAMTRU1",
            "name": "Thẻ tạm trú 1"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    },
    {
        "reference_flag": False,
        "created_date": "2021-02-18",
        "identity_document_type": {
            "id": "2",
            "code": "THETAMTRU2",
            "name": "Thẻ tạm trú 2"
        },
        "identity_images": [
            {
                "image_url": "https://example.com/example.jpg"
            }
        ]
    }
]


async def repos_get_detail_sub_identity(cif_id: str, session: Session):
    sub_identities = session.execute(
        select(
            CustomerSubIdentity,
            CustomerSubIdentityType,
            PlaceOfIssue,
            CustomerIdentityImage
        )
        .join(CustomerSubIdentityType, CustomerSubIdentity.sub_identity_type_id == CustomerSubIdentityType.id)
        .join(PlaceOfIssue, CustomerSubIdentity.place_of_issue_id == PlaceOfIssue.id)
        .join(CustomerIdentityImage, CustomerSubIdentity.id == CustomerIdentityImage.identity_id)
        .filter(CustomerSubIdentity.customer_id == cif_id)
    ).all()

    if not sub_identities:
        return ReposReturn(is_error=True, msg=ERROR_SUB_IDENTITY_DOCUMENT_NOT_EXIST, loc="cif_id")

    data = []
    for sub_identity, sub_identity_type, place_of_issue, customer_identity_image in sub_identities:
        data.append({
            "id": sub_identity.id,
            "name": sub_identity.name,
            "sub_identity_document_type": dropdown(sub_identity_type),
            "sub_identity_document_image_url": customer_identity_image.image_url,
            "ocr_result": {
                "sub_identity_number": sub_identity.number,
                "symbol": sub_identity.symbol,
                "full_name_vn": sub_identity.full_name,
                "date_of_birth": sub_identity.date_of_birth,
                "passport_number": sub_identity.passport_number,
                "place_of_issue": dropdown(place_of_issue),
                "expired_date": sub_identity.sub_identity_expired_date,
                "issued_date": sub_identity.issued_date
            }
        })
    return ReposReturn(data=data)


@auto_commit
async def repos_save_sub_identity(
        customer: Customer,
        delete_sub_identity_ids: List,
        create_sub_identities: List,
        create_sub_identity_images: List,
        create_customer_sub_identity_image_transactions: List,
        update_sub_identities: List,
        update_sub_identity_images: List,
        update_customer_sub_identity_image_transactions: List,
        session: Session,
        log_data: json
):

    # Xóa
    if delete_sub_identity_ids:
        session.execute(delete(CustomerSubIdentity).filter(
            CustomerSubIdentity.id.in_(delete_sub_identity_ids)
        ))

    # Tạo giấy tờ định danh phụ
    session.bulk_save_objects([CustomerSubIdentity(**customer_sub_identity)
                               for customer_sub_identity in create_sub_identities])

    session.bulk_save_objects([CustomerIdentityImage(**create_sub_identity_image)
                               for create_sub_identity_image in create_sub_identity_images])
    # lưu log cho lịch sử thay đổi giấy tờ định danh phụ khi tạo mới
    session.bulk_save_objects([CustomerIdentityImageTransaction(**customer_identity_image_transaction)
                              for customer_identity_image_transaction in create_customer_sub_identity_image_transactions])

    # Cập nhật
    session.bulk_update_mappings(CustomerSubIdentity, update_sub_identities)
    session.bulk_update_mappings(CustomerIdentityImage, update_sub_identity_images)
    # lưu log cho lịch sử thay đổi giấy tờ định danh phụ khi cập nhật
    session.bulk_save_objects([CustomerIdentityImageTransaction(**customer_identity_image_transaction)
                               for customer_identity_image_transaction in update_customer_sub_identity_image_transactions])

    # Lưu lại Log lịch sử giao dịch trong ngày
    is_success, booking_response = await write_transaction_log_and_update_booking(
        log_data=log_data,
        session=session,
        customer_id=customer.id,
        business_form_id=BUSINESS_FORM_TTCN_GTDD_GTDDP
    )
    if not is_success:
        return ReposReturn(is_error=True, msg=booking_response['msg'])

    return ReposReturn(data={
        "cif_id": customer.id
    })


async def repos_get_sub_identity_log_list(
        cif_id: str,
        session: Session
) -> ReposReturn:

    sub_identity_image_transactions = session.execute(
        select(
            CustomerIdentityImageTransaction,
        )
        .join(CustomerIdentityImage, CustomerIdentityImageTransaction.identity_image_id == CustomerIdentityImage.id)
        .join(CustomerSubIdentity, and_(
            CustomerIdentityImage.identity_id == CustomerSubIdentity.id,
            CustomerSubIdentity.customer_id == cif_id
        ))
        .order_by(desc(CustomerIdentityImageTransaction.maker_at))
    ).scalars().all()

    return ReposReturn(data=sub_identity_image_transactions)


########################################################################################################################
# Other
########################################################################################################################
async def repos_get_sub_identities_and_sub_identity_images(customer_id: str, session: Session):
    sub_identities = session.execute(
        select(
            CustomerSubIdentity,
            CustomerIdentityImage
        )
        .join(CustomerIdentityImage, and_(
            CustomerSubIdentity.id == CustomerIdentityImage.identity_id,
            CustomerIdentityImage.image_type_id == IMAGE_TYPE_CODE_SUB_IDENTITY
        ))
        .filter(
            CustomerSubIdentity.customer_id == customer_id
        )
    ).all()

    return ReposReturn(data=sub_identities)
