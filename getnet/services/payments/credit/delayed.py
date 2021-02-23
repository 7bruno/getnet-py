class CreditConfirm:
    def __init__(self, confirm_date, message):

        self.confirm_date = confirm_date
        self.message = message


class DelayedResponse:

    def __init__(self, payment_id: str, seller_id: str, amount: int, currency: str, order_id: str, status: str, credit_confirm: dict):

        self.payment_id = payment_id
        self.seller_id = seller_id
        self.amount = amount
        self.currency = currency
        self.order_id = order_id
        self.status = status
        self.credit_confirm = CreditConfirm(**credit_confirm)


class DelayedAdjustResponse:

    def __init__(
        self,
        payment_id: str,
        seller_id: str,
        amount: int,
        currency: str,
        order_id: str,
        status: str,
        authorization_code: str,
        authorized_at: str,
        reason_code: str,
        reason_message: str,
        acquirer: str,
        soft_descriptor: str,
        terminal_nsu: str,
        acquirer_transaction_id: str,
        adjustment_acquirer_transactiion_id: str
    ):

        self.payment_id = payment_id
        self.seller_id = seller_id
        self.amount = amount
        self.currency = currency
        self.order_id = order_id
        self.status = status
        self.authorization_code = authorization_code
        self.authorized_at = authorized_at
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.acquirer = acquirer
        self.soft_descriptor = soft_descriptor
        self.terminal_nsu = terminal_nsu
        self.acquirer_transaction_id = acquirer_transaction_id
        self.adjustment_acquirer_transactiion_id = adjustment_acquirer_transactiion_id
