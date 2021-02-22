from getnet.services.payments import Customer
from getnet.services.payments.boleto.boleto import Boleto
from getnet.services.payments.boleto.boleto_response import BoletoPaymentResponse
from getnet.services.payments.marketplace_subseller import MarketplaceSubseller
from getnet.services.payments.order import Order
from getnet.services.service import Service


class BoletoService(Service):
    path = "/v1/payments/boleto"

    def create(
        self,
        amount: int,
        currency: str,
        order: Order,
        boleto: Boleto,
        customer: Customer,
    ) -> BoletoPaymentResponse:
        data = {
            "seller_id": self._client.seller_id,
            "amount": amount,
            "currency": currency,
            "order": order.as_dict(),
            "boleto": boleto.as_dict(),
            "customer": customer.as_dict(),
        }

        response = self._post(self._format_url(), json=data)
        return BoletoPaymentResponse(_base_uri=self._client.base_url, **response)

    def marketplaceBoletoCreate(
        self,
        amount: int,
        currency: str,
        order: Order,
        boleto: Boleto,
        customer: Customer,
        marketplace_subseller_payments: MarketplaceSubseller
    ) -> BoletoPaymentResponse:
        data = {
            "seller_id": self._client.seller_id,
            "amount": amount,
            "currency": currency,
            "order": order.as_dict(),
            "boleto": boleto.as_dict(),
            "customer": customer.as_dict(),
        }

        if marketplace_subseller_payments is not None:

            data["marketplace_subseller_payments"] = marketplace_subseller_payments

        data["customer"]["billing_address"] = data["customer"].pop("address")
        data["customer"]["billing_address"].pop("country")
        data["customer"].pop("observation")
        phone = data["customer"].pop("phone_number")
        cellphone = data["customer"].pop("celphone_number")
        data["customer"].pop("seller_id")
        data["customer"].pop("customer_id")
        data["customer"].pop("email")
        data["customer"].pop("birth_date")
        data["customer"].setdefault(
            "name", f'{data["customer"]["first_name"]} {data["customer"]["last_name"]}')

        data["boleto"].pop("our_number")

        print(data)

        response = self._post(self._format_url(), json=data)
        return BoletoPaymentResponse(_base_uri=self._client.base_url, **response)
