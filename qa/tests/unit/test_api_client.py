from unittest.mock import Mock

import pytest

from utils.api_client import ApiClient


@pytest.fixture
def api_client():
    client = ApiClient(base_url="http://api.example.test/")
    client.session = Mock()
    client.session.headers = {}
    return client


def test_constructor_normalizes_base_url_and_sets_initial_token():
    initial_token = "dummy-token"
    client = ApiClient(base_url="http://api.example.test/", token=initial_token)

    assert client.base_url == "http://api.example.test"
    assert client.session.verify is True
    assert client.session.headers["Authorization"] == f"Bearer {initial_token}"


def test_login_stores_token_on_success(api_client):
    response = Mock(status_code=200)
    response.json.return_value = {"access_token": "new-token"}
    api_client.session.post.return_value = response

    result = api_client.login("user@example.test", "password")

    assert result is response
    api_client.session.post.assert_called_once_with(
        "http://api.example.test/api/auth/token",
        data={"username": "user@example.test", "password": "password"},
        timeout=10,
    )
    assert api_client.session.headers["Authorization"] == "Bearer new-token"


def test_login_does_not_store_token_on_failure(api_client):
    response = Mock(status_code=401)
    api_client.session.post.return_value = response

    result = api_client.login("user@example.test", "wrong-password")

    assert result is response
    assert "Authorization" not in api_client.session.headers


@pytest.mark.parametrize(
    ("method", "kwargs"),
    [
        ("get", {"params": {"page": 2}}),
        ("post", {"json": {"name": "event"}}),
        ("put", {"json": {"name": "updated event"}}),
        ("patch", {"json": {"name": "patched event"}}),
    ],
)
def test_http_methods_forward_url_and_arguments(api_client, method, kwargs):
    response = Mock()
    request = getattr(api_client.session, method)
    request.return_value = response

    result = getattr(api_client, method)("/api/events", **kwargs)

    assert result is response
    request.assert_called_once_with("http://api.example.test/api/events", **kwargs)


@pytest.mark.parametrize(
    ("promo_code", "expected_payload"),
    [
        (None, {"event_id": 12, "items": [{"category_id": 3, "quantity": 2}]}),
        (
            "WELCOME10",
            {"event_id": 12, "items": [{"category_id": 3, "quantity": 2}], "promo_code": "WELCOME10"},
        ),
    ],
)
def test_create_order_builds_payload(api_client, promo_code, expected_payload):
    response = Mock()
    api_client.session.post.return_value = response

    result = api_client.create_order(12, [{"category_id": 3, "quantity": 2}], promo_code)

    assert result is response
    api_client.session.post.assert_called_once_with(
        "http://api.example.test/api/orders",
        json=expected_payload,
    )


def test_pay_sends_payment_details(api_client):
    response = Mock()
    api_client.session.post.return_value = response

    result = api_client.pay(42, "4242 4242 4242 4242")

    assert result is response
    api_client.session.post.assert_called_once_with(
        "http://api.example.test/api/orders/42/pay",
        json={
            "card_number": "4242 4242 4242 4242",
            "exp_month": 12,
            "exp_year": 2030,
            "cvc": "123",
            "cardholder": "QA Bot",
        },
    )
