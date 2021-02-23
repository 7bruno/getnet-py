from typing import Union
from uuid import UUID

from getnet.services.payments import Customer
from getnet.services.payments import OrderItem
from getnet.services.payments.marketplace_subseller import MarketplaceSubseller
from getnet.services.payments.credit.delayed import DelayedResponse

from getnet.services.payments.credit.credit import Credit
from getnet.services.payments.credit.credit_cancel import CreditCancelPaymentResponse
from getnet.services.payments.credit.credit_response import CreditPaymentResponse
from getnet.services.payments.order import Order
from getnet.services.service import Service
from getnet.services.utils import Device


class CreditPaymentService(Service):
    path = "/v1/payments/credit"

    def create(
        self,
        amount: int,
        currency: str,
        order: Order,
        credit: Credit,
        customer: Customer,
        device: Device = None,
    ) -> CreditPaymentResponse:
        data = {
            "seller_id": self._client.seller_id,
            "amount": amount,
            "currency": currency,
            "order": order.as_dict(),
            "customer": customer.as_dict(),
            "credit": credit.as_dict(),

        }

        if device is not None:
            data["device"] = device.as_dict()

        response = self._post(self._format_url(), json=data)
        return CreditPaymentResponse(**response)

    def cancel(self, payment_id: Union[UUID, str]) -> CreditCancelPaymentResponse:
        response = self._post(
            self._format_url(path="/{payment_id}/cancel",
                             payment_id=str(payment_id))
        )
        return CreditCancelPaymentResponse(**response)

    def marketplaceCreditCreate(
        self,
        marketplace_subseller_payments: list,
        amount: int,
        order: Order,
        customer: Customer,
        credit: Credit,
        currency: str = "BRL",
        device: Device = None
    ):

        data = {
            "seller_id": self._client.seller_id,
            "amount": amount,
            "currency": currency,
            "order": order.as_dict(),
            "customer": customer.as_dict(),
            "credit": credit.as_dict()
        }

        if marketplace_subseller_payments is not None:

            data["marketplace_subseller_payments"] = marketplace_subseller_payments

        if device is not None:
            data["device"] = device.as_dict()

        data["credit"].pop("authenticated")
        data["customer"]["billing_address"] = data["customer"].pop("address")
        data["customer"].pop("observation")
        phone = data["customer"].pop("phone_number")
        cellphone = data["customer"].pop("celphone_number")
        data["customer"].pop("seller_id")
        data["customer"].pop("birth_date")
        data["customer"].setdefault(
            "name", f'{data["customer"]["first_name"]} {data["customer"]["last_name"]}')

        data["shippings"] = [{
            "first_name": data["customer"]["first_name"],
            "name": f'{data["customer"]["first_name"]} {data["customer"]["last_name"]}',
            "email":data["customer"]["email"],
            "phone_number":cellphone,
            "shipping_amount": 0,
            "address":data["customer"]["billing_address"]
        }]

        response = self._post(self._format_url(), json=data)

        return CreditPaymentResponse(**response)

    def delayed(self, payment_id: Union[UUID, str], amount: int, marketplace_subseller_payments: list = None):

        data = {
            "amount": amount,
        }

        if marketplace_subseller_payments:

            data["marketplace_subseller_payments"] = marketplace_subseller_payments

        response = self._post(self._format_url() +
                              f'/{payment_id}/confirm', json=data)

        return DelayedResponse(**response)

    def delayedAdjust(self, payment_id: Union[UUID, str], amount: int, currency: str = "BRL", marketplace_subseller_payments: list = None):

        data = {
            "amount": amount,
            "currency": currency
        }

        if marketplace_subseller_payments:

            data["marketplace_subseller_payments"] = marketplace_subseller_payments

        response = self._post(self._format_url() +
                              f'/{payment_id}/adjustment', json=data)

        return DelayedAdjustResponse(**response)
