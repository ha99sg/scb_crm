from app.api.base.repository import ReposReturn
from app.settings.event import service_gw


async def repos_gw_payment_amount_block(current_user, data_input):

    is_success, gw_payment_amount_block = await service_gw.gw_payment_amount_block(
        current_user=current_user.user_info, data_input=data_input
    )
    amount_block_out = gw_payment_amount_block.get('amountBlock_out', {})

    # check trường hợp lỗi
    if not amount_block_out.get('data_output', {}):
        return ReposReturn(is_error=True, msg=amount_block_out.get('transaction_info').get('transaction_error_msg'))

    return ReposReturn(data=gw_payment_amount_block)
