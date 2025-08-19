# api/api_client.py
from playwright.sync_api import Page, expect

# This is a good practice for defining the base URL in a central place.
BASE_URL = 'https://fakestoreapi.com'

class ApiClient:
    """
    This class encapsulates all API interactions with the Fake Store API.
    It separates the test logic from the API implementation details.
    """

    def __init__(self, page: Page):
        """
        Initializes the ApiClient with the Playwright Page object.
        """
        self.page = page
    
    def login(self, username, password):
        """
        Performs a login request and returns the response.
        """
        credentials = {'username': username, 'password': password}
        response = self.page.request.post(f'{BASE_URL}/auth/login', data=credentials)
        return response

    def get_single_product(self, product_id):
        """
        Fetches a single product by its ID.
        """
        response = self.page.request.get(f'{BASE_URL}/products/{product_id}')
        return response

    def get_all_products(self):
        """
        Fetches all products from the API.
        """
        response = self.page.request.get(f'{BASE_URL}/products')
        return response

    def create_product(self, product_data, token):
        """
        Creates a new product with authentication.
        """
        headers = {"Authorization": f"Bearer {token}"}
        response = self.page.request.post(f'{BASE_URL}/products', data=product_data, headers=headers)
        return response