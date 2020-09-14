from datetime import timedelta, datetime

import pytest
from pytest_mock import MockerFixture

from getnet import Client
from getnet.errors import RequestError
from getnet.services import token
from getnet.services.token.card_token import CardToken


@pytest.fixture
def client():
    return Client(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "388183f9-ab04-4c21-9234",
        )

class TestClientAuth:
    def test_invalid_data(self, client: Client, mocker: MockerFixture) -> None:
        sessionGetMock = mocker.patch("requests.Session.get", return_value=mocker.MagicMock())
        sessionGetMock.ok.return_value = False

        with pytest.raises(RequestError):
            client.auth()

    def test_missing_access_token(self, client: Client, mocker: MockerFixture) -> None:
        mocker.patch("getnet.Client.auth", return_value=True)
        sessionGetMock = mocker.patch("requests.Session.get", return_value=mocker.MagicMock())
        sessionGetMock.ok.return_value = True

        access_token_expired = mocker.spy(client, 'access_token_expired')
        client.access_token = None

        client.get("/test")
        access_token_expired.assert_called_once()
        client.auth.assert_called_once()

    def test_expired_access_token(self, client: Client, mocker: MockerFixture) -> None:
        mocker.patch("getnet.Client.auth", return_value=True)
        sessionGetMock = mocker.patch("requests.Session.get", return_value=mocker.MagicMock())
        sessionGetMock.ok.return_value = True

        access_token_expired = mocker.spy(client, 'access_token_expired')
        client.access_token = "test"
        client.access_token_expires = int(datetime.timestamp(datetime.now() + timedelta(seconds=-3600)))

        client.get("/test")
        access_token_expired.assert_called_once()
        client.auth.assert_called_once()


class TestClient:
    def test_invalid_environment(self):
        with pytest.raises(AttributeError):
            Client("a", "b", "c", "10")

    def test_token_service(self, client: Client, mocker: MockerFixture) -> None:
        mocker.patch("getnet.Client.auth", return_value=True)

        assert isinstance(client.token_service(), token.Service)

    def test_generate_token_card_shortcut(self, client: Client, mocker: MockerFixture):
        mocker.patch("getnet.Client.auth", return_value=True)
        tokenServiceMock = mocker.patch.object(token.Service, "generate")
        tokenServiceMock.return_value = CardToken("123")

        response = client.generate_token_card("5155901222280001", "customer_21081826")

        assert response.number_token == "123"
        tokenServiceMock.assert_called_once()
