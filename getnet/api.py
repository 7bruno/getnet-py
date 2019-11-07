import logging
from datetime import datetime, timedelta

import requests
from requests import HTTPError

from getnet.exceptions import *

__all__ = ['LOGGER', 'SANDBOX', 'HOMOLOG', 'PRODUCTION', 'Client', 'API']

SANDBOX = 0
HOMOLOG = 1
PRODUCTION = 2

ENVIRONMENTS = (SANDBOX, HOMOLOG, PRODUCTION)

API_URLS = {
    SANDBOX: "https://api-sandbox.getnet.com.br",
    HOMOLOG: "https://api-homologacao.getnet.com.br",
    PRODUCTION: "https://api.getnet.com.br",
}

LOGGER = logging.getLogger("getnet-py")


class handler_request:
    def __init__(self, client: 'Client'):
        self.client = client

    def __enter__(self):
        if self.client._access_token_expired():
            self.client.auth()

        return LOGGER

    def __exit__(self, exc_type, exc_val, exc_tb):
        return not isinstance(exc_val, GetnetException)


def handler_request_exception(error: HTTPError):
    status_code = error.response.status_code
    message = u"{} {} ({})".format(
        error.response.status_code,
        error.response.json().get("message"),
        error.response.url,
    )
    kwargs = {
        'request': error.request,
        'response': error.response
    }

    if status_code == 400:
        return BadRequest(message, )
    elif status_code == 402:
        return BusinessError(message, **kwargs)
    elif status_code == 404:
        return NotFound(message, **kwargs)
    elif status_code == 500:
        return ServerError(message, **kwargs)
    elif status_code == 503:
        return ServiceUnavailable(message, **kwargs)
    elif status_code == 504:
        return GatewayTimeout(message, **kwargs)
    else:
        return GetnetException(message, **kwargs)


class Client:
    request: requests.Session
    seller_id: str = None
    client_id: str = None
    client_secret: str = None
    environment: int = 0
    access_token: str = None
    access_token_expires: int = None

    def __init__(
        self,
        seller_id: str,
        client_id: str,
        client_secret: str,
        environment: int = SANDBOX,
    ):
        self.seller_id = seller_id
        self.client_id = client_id
        self.client_secret = client_secret

        if environment not in ENVIRONMENTS:
            raise GetnetException('Invalid environment')

        self.environment = environment
        self.base_url = API_URLS[environment]

        self._setup_client()

    def _setup_client(self):
        self.request = requests.Session()
        self.request.headers.update({"user-agent": "getnet-py/1.0"})
        self.auth()

    def _access_token_expired(self):
        return self.access_token is not None and \
               self.access_token_expires > datetime.timestamp(datetime.now())

    def _handler_request(self):
        return handler_request(self)

    def auth(self) -> None:
        if not self.access_token or self._access_token_expired():
            path = "/auth/oauth/v2/token"
            data = {"scope": "oob", "grant_type": "client_credentials"}

            try:
                response = self.request.post(self.base_url + path,
                                             data=data,
                                             auth=(self.client_id, self.client_secret)
                )
                response.raise_for_status()

                self.access_token = response.json().get("access_token")
                self.access_token_expires = int(datetime.timestamp(datetime.now() + timedelta(seconds=response.json().get('expires_in'))))
                self.request.headers.update(
                    {"Authorization": "Bearer {}".format(self.access_token)}
                )
            except HTTPError as err:
                raise handler_request_exception(err)

    def get(self, path, **kwargs):
        with self._handler_request():
            url = self.base_url + path
            try:
                response = self.request.get(url, **kwargs)
                response.raise_for_status()
                return response.json()
            except HTTPError as err:
                raise handler_request_exception(err)

    def post(self, path: str, **kwargs):
        with self._handler_request():
            url = self.base_url + path
            try:
                response = self.request.post(url, **kwargs)
                response.raise_for_status()
                return response.json()
            except HTTPError as err:
                raise handler_request_exception(err)

    def delete(self, path: str, **kwargs):
        with self._handler_request():
            url = self.base_url + path
            try:
                response = self.request.delete(url, **kwargs)
                response.raise_for_status()
                return response.json()
            except HTTPError as err:
                raise handler_request_exception(err)

    # def generate_token_card(self, card_number: str, customer_id: str):
    #     return services.TokenCardService(self).create(card_number, customer_id)
    #
    # def cards(self):
    #     return services.CardService(self)
    #
    # def customers(self):
    #     return services.CustomerService(self)
    #
    # def payment(self, type: str):
    #     if type == "boleto":
    #         return PaymentBoletoService(self)
    #     elif type == "credit":
    #         return PaymentCreditService(self)
    #     elif type == "cancel":
    #         return PaymentCancelService(self)


# Discontinued = Will be removed in 1.1
# @todo remove in version 1.1
API = Client
