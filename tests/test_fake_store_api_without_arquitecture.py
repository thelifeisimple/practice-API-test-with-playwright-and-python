import pytest

# The 'page' fixture is provided by the pytest-playwright plugin.
# It includes the 'request' object for making API calls.
from playwright.sync_api import Page, expect

# This is the base URL for the API we are testing.
# It's a good practice to define this as a constant.
BASE_URL = 'https://fakestoreapi.com'

# This fixture will store the token for authenticated requests
@pytest.fixture(scope="function")
def auth_token(page: Page):
    """
    A fixture to log in and get an authentication token for the session.
    This token can then be used in other tests.
    
    NOTE: The scope was changed from "session" to "function" to fix the
    ScopeMismatch error, as this fixture depends on the 'page' fixture
    which has a function scope.
    """
    credentials = {'username': 'mor_2314', 'password': '83r5^_'}
    response = page.request.post(f'{BASE_URL}/auth/login', data=credentials)
    assert response.status == 201, f"Failed to log in. Status: {response.status}"
    response_json = response.json()
    assert 'token' in response_json, "Login response missing 'token'"
    return response_json['token']


def test_api_login(page: Page):
    """
    Tests a successful API login and verifies the response.
    We check for a 200 status code and the presence of a 'token'.
    """
    credentials = {'username': 'mor_2314', 'password': '83r5^_'}
    response = page.request.post(f'{BASE_URL}/auth/login', data=credentials)

    # Use a clear assertion for the status code.
    expect(response).to_be_ok()

    # Get the JSON body and verify the token.
    response_json = response.json()
    assert 'token' in response_json, "Response JSON is missing the 'token' field"
    print(f"Login successful. Token received: {response_json['token']}")


def test_get_single_product(page: Page):
    """
    Tests a basic GET request to fetch a product by its ID.
    We verify the status code and the data in the response body.
    """
    product_id = 1
    response = page.request.get(f'{BASE_URL}/products/{product_id}')

    # Verify the status code.
    expect(response).to_be_ok()

    # Verify the product data in the JSON response.
    response_json = response.json()
    assert response_json['id'] == product_id, "Product ID in response does not match request"
    assert 'title' in response_json, "Product is missing a 'title' field"
    print(f"Product fetched: {response_json['title']}")



def test_api_login_with_invalid_credentials(page: Page):
    """
    Tests a failed login with invalid credentials to ensure proper error handling.
    """
    invalid_credentials = {'username': 'pepito', 'password': 'wrong_password'}
    response = page.request.post(f'{BASE_URL}/auth/login', data=invalid_credentials)

    # We expect a 401 Unauthorized status code for invalid credentials.
    assert response.status == 401, f"Expected 401 Unauthorized, but got {response.status}"

    # The API returns a plain text string for this case, not JSON.
    # We use response.text() to get the string content.
    response_text = response.text()
    
    # Assert that the text matches the expected error message.
    assert response_text == 'username or password is incorrect', "Unexpected error message"
    print(f"Login failed as expected with message: '{response_text}'")


def test_get_all_products(page: Page):
    """
    This test gets all products and verifies the response is a list
    and contains a certain number of items. This demonstrates a more
    realistic validation of an API response.
    """
    response = page.request.get(f'{BASE_URL}/products')

    expect(response).to_be_ok()

    response_json = response.json()
    assert isinstance(response_json, list), "Response is not a list"
    assert len(response_json) == 20, "Expected 20 products in the list"
    print(f"Successfully fetched {len(response_json)} products.")


def test_create_a_product(page: Page, auth_token):
    """
    This test demonstrates a POST request that requires authentication.
    It uses the token from the 'auth_token' fixture to post a new product.
    Note: The fakestoreapi.com is a mock API, so the product won't actually be created.
    """
    new_product_data = {
        "title": "A new product",
        "price": 100,
        "description": "An awesome new gadget.",
        "category": "electronics"
    }

    # The auth_token fixture provides the token, which we add to the headers.
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = page.request.post(f'{BASE_URL}/products', data=new_product_data, headers=headers)

    expect(response).to_be_ok()
    
    response_json = response.json()
    assert 'id' in response_json, "New product response is missing an 'id'"
    assert response_json['title'] == new_product_data['title'], "New product title mismatch"
    print(f"Successfully created product with ID: {response_json['id']}")

