# conftest.py
import pytest
from playwright.sync_api import Page
from api.api_client import ApiClient

@pytest.fixture(scope="function")
def api_client(page: Page):
    """
    A fixture that provides a single instance of the ApiClient
    for each test function.
    """
    return ApiClient(page)

@pytest.fixture(scope="function")
def auth_token(api_client: ApiClient):
    """
    A fixture to log in using the ApiClient and get a token.
    It now uses the api_client fixture, separating the login logic.
    """
    credentials = {'username': 'mor_2314', 'password': '83r5^_'}
    response = api_client.login(**credentials)
    assert response.status == 201, f"Failed to log in. Status: {response.status}"
    response_json = response.json()
    assert 'token' in response_json, "Login response missing 'token'"
    return response_json['token']