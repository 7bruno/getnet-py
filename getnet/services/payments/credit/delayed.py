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
