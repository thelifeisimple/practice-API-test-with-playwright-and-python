# tests/test_api_login.py
#import fixtures from conftest.py
import pytest
from playwright.sync_api import Page, expect
from api.api_client import ApiClient, BASE_URL

def test_api_login(api_client: ApiClient):
    """
    Tests a successful API login using the new ApiClient.
    """
    credentials = {'username': 'mor_2314', 'password': '83r5^_'}
    response = api_client.login(**credentials)
    expect(response).to_be_ok()
    response_json = response.json()
    assert 'token' in response_json, "Response JSON is missing the 'token' field"
    print(f"Login successful. Token received: {response_json['token']}")


def test_get_single_product(api_client: ApiClient):
    """
    Tests fetching a single product using the ApiClient.
    """
    product_id = 1
    response = api_client.get_single_product(product_id)
    expect(response).to_be_ok()
    response_json = response.json()
    assert response_json['id'] == product_id, "Product ID in response does not match request"
    assert 'title' in response_json, "Product is missing a 'title' field"
    print(f"Product fetched: {response_json['title']}")


def test_api_login_with_invalid_credentials(api_client: ApiClient):
    """
    Tests a failed login with invalid credentials to ensure proper error handling.
    """
    invalid_credentials = {'username': 'pepito', 'password': 'wrong_password'}
    response = api_client.login(**invalid_credentials)
    assert response.status == 401, f"Expected 401 Unauthorized, but got {response.status}"
    response_text = response.text()
    assert response_text == 'username or password is incorrect', "Unexpected error message"
    print(f"Login failed as expected with message: '{response_text}'")


def test_get_all_products(api_client: ApiClient):
    """
    This test gets all products and verifies the response is a list.
    """
    response = api_client.get_all_products()
    expect(response).to_be_ok()
    response_json = response.json()
    assert isinstance(response_json, list), "Response is not a list"
    assert len(response_json) == 20, "Expected 20 products in the list"
    print(f"Successfully fetched {len(response_json)} products.")


def test_create_a_product(api_client: ApiClient, auth_token):
    """
    This test demonstrates a POST request that requires authentication.
    It uses the token from the 'auth_token' fixture to post a new product.
    """
    new_product_data = {
        "title": "A new product",
        "price": 100,
        "description": "An awesome new gadget.",
        "category": "electronics"
    }
    response = api_client.create_product(new_product_data, auth_token)
    expect(response).to_be_ok()
    response_json = response.json()
    assert 'id' in response_json, "New product response is missing an 'id'"
    assert response_json['title'] == new_product_data['title'], "New product title mismatch"
    print(f"Successfully created product with ID: {response_json['id']}")