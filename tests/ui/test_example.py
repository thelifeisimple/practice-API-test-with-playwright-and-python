# test_example.py
import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    """
    A simple test to check the title of a page.
    The 'page' fixture is automatically provided by the pytest-playwright plugin.
    """
    page.goto("https://playwright.dev/")
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    """
    A test to click a link and verify the new page content.
    """
    page.goto("https://playwright.dev/")
    
    # Click the "Get started" link.
    page.get_by_role("link", name="Get started").click()
    
    # Expect the page to have a heading with the name of "Installation".
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()