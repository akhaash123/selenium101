import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# =========================================================
# TEST CONFIGURATION
# =========================================================

BASE_URL = "https://www.testmuai.com/selenium-playground/"
MESSAGE = "Welcome to TestMu AI"


# =========================================================
# TESTMU AI / LAMBDATEST CREDENTIALS
# =========================================================
#
# These values come from your TestMu AI Credentials page.
#
# DO NOT put the actual Access Key directly into this file
# if you are going to upload the project to GitHub.
#
# We will set these through PowerShell before running pytest.
# =========================================================

LT_USERNAME = os.getenv("LT_USERNAME")
LT_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")


# =========================================================
# BROWSER / OS CONFIGURATIONS
# =========================================================

BROWSER_CONFIGS = [
    {
        "browser": "Chrome",
        "browser_version": "latest",
        "platform": "Windows 11",
    },
    {
        "browser": "Firefox",
        "browser_version": "latest",
        "platform": "Linux",
    },
]


# =========================================================
# REMOTE SELENIUM FIXTURE
# =========================================================

@pytest.fixture(params=BROWSER_CONFIGS)
def driver(request):

    config = request.param

    browser = config["browser"]
    browser_version = config["browser_version"]
    platform = config["platform"]

    # -----------------------------------------------------
    # Check credentials
    # -----------------------------------------------------

    if not LT_USERNAME:
        raise RuntimeError(
            "LT_USERNAME is not set. "
            "Set it in PowerShell before running pytest."
        )

    if not LT_ACCESS_KEY:
        raise RuntimeError(
            "LT_ACCESS_KEY is not set. "
            "Set it in PowerShell before running pytest."
        )

    # -----------------------------------------------------
    # Create browser-specific Selenium options
    # -----------------------------------------------------

    if browser.lower() == "chrome":

        options = webdriver.ChromeOptions()

    elif browser.lower() == "firefox":

        options = webdriver.FirefoxOptions()

    else:

        raise ValueError(
            f"Unsupported browser: {browser}"
        )

    # -----------------------------------------------------
    # Browser configuration
    # -----------------------------------------------------

    options.set_capability(
        "browserName",
        browser
    )

    options.set_capability(
        "browserVersion",
        browser_version
    )

    # -----------------------------------------------------
    # TestMu AI / LambdaTest capabilities
    # -----------------------------------------------------

    lt_options = {

        "platformName": platform,

        "build": "TestMu AI Selenium Assignment",

        "project": "Selenium Playground",

        "name": (
            f"{request.node.name} - "
            f"{browser} - "
            f"{platform}"
        ),

        # -------------------------------------------------
        # Assignment requirements
        # -------------------------------------------------

        "video": True,

        "network": True,

        "console": True,

        # -------------------------------------------------
        # Selenium / pytest
        # -------------------------------------------------

        "w3c": True,

        "plugin": "pytest",
    }

    options.set_capability(
        "LT:Options",
        lt_options
    )

    # -----------------------------------------------------
    # LambdaTest / TestMu AI Selenium Grid
    # -----------------------------------------------------
    #
    # Credentials are included in the Grid URL.
    # This fixes the 401 Authorization Required issue
    # when the credentials are not being accepted from
    # LT:Options.
    # -----------------------------------------------------

    grid_url = (
        f"https://{LT_USERNAME}:{LT_ACCESS_KEY}"
        "@hub.lambdatest.com/wd/hub"
    )

    # -----------------------------------------------------
    # Start remote browser
    # -----------------------------------------------------

    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )

    # -----------------------------------------------------
    # Implicit wait
    # -----------------------------------------------------

    driver.implicitly_wait(5)

    # -----------------------------------------------------
    # Give driver to the test
    # -----------------------------------------------------

    yield driver

    # -----------------------------------------------------
    # Close remote session
    # -----------------------------------------------------

    driver.quit()


# =========================================================
# TEST SCENARIO 1 - SIMPLE FORM DEMO
# =========================================================

def test_simple_form_demo(driver):

    driver.get(BASE_URL)

    driver.find_element(
        By.LINK_TEXT,
        "Simple Form Demo"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("simple-form-demo")
    )

    assert "simple-form-demo" in driver.current_url

    message_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "user-message")
        )
    )

    message_box.clear()

    message_box.send_keys(MESSAGE)

    driver.find_element(
        By.ID,
        "showInput"
    ).click()

    result = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "message")
        )
    )

    assert result.text == MESSAGE


# =========================================================
# TEST SCENARIO 2 - DRAG & DROP SLIDERS
# =========================================================

def test_drag_drop_slider(driver):

    driver.get(BASE_URL)

    driver.find_element(
        By.LINK_TEXT,
        "Drag & Drop Sliders"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("drag-drop-range-sliders")
    )

    slider = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@type='range' and @value='15']"
            )
        )
    )

    driver.execute_script(
        """
        arguments[0].value = '95';

        arguments[0].dispatchEvent(
            new Event('input', {bubbles: true})
        );

        arguments[0].dispatchEvent(
            new Event('change', {bubbles: true})
        );
        """,
        slider
    )

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(
            "return arguments[0].value;",
            slider
        ) == "95"
    )

    actual_value = driver.execute_script(
        "return arguments[0].value;",
        slider
    )

    assert actual_value == "95"


# =========================================================
# TEST SCENARIO 3 - INPUT FORM SUBMIT
# =========================================================

def test_input_form_submit(driver):

    driver.get(BASE_URL)

    # -----------------------------------------------------
    # Click Input Form Submit
    # -----------------------------------------------------

    driver.find_element(
        By.XPATH,
        "//a[normalize-space()='Input Form Submit']"
    ).click()

    # -----------------------------------------------------
    # Wait for Name field
    # -----------------------------------------------------

    name = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.NAME, "name")
        )
    )

    # -----------------------------------------------------
    # Fill Name
    # -----------------------------------------------------

    name.clear()

    name.send_keys("Test User")

    # -----------------------------------------------------
    # Email
    # -----------------------------------------------------

    email = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "inputEmail4")
        )
    )

    email.clear()

    email.send_keys(
        "testuser@example.com"
    )

    # -----------------------------------------------------
    # Password
    # -----------------------------------------------------

    password = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.NAME, "password")
        )
    )

    password.clear()

    password.send_keys(
        "Password123"
    )

    # -----------------------------------------------------
    # Company
    # -----------------------------------------------------

    company = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "company")
        )
    )

    company.clear()

    company.send_keys(
        "TestMu AI"
    )

    # -----------------------------------------------------
    # Website
    # -----------------------------------------------------

    website = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "websitename")
        )
    )

    website.clear()

    website.send_keys(
        "https://www.testmuai.com"
    )

    # -----------------------------------------------------
    # Country
    # -----------------------------------------------------

    country = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.NAME, "country")
        )
    )

    Select(country).select_by_value("US")

    # -----------------------------------------------------
    # City
    # -----------------------------------------------------

    city = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "inputCity")
        )
    )

    city.clear()

    city.send_keys(
        "New York"
    )

    # -----------------------------------------------------
    # Address 1
    # -----------------------------------------------------

    address1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "inputAddress1")
        )
    )

    address1.clear()

    address1.send_keys(
        "123 Test Street"
    )

    # -----------------------------------------------------
    # Address 2
    # -----------------------------------------------------

    address2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "inputAddress2")
        )
    )

    address2.clear()

    address2.send_keys(
        "Apartment 101"
    )

    # -----------------------------------------------------
    # State
    # -----------------------------------------------------

    state = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "inputState")
        )
    )

    state.clear()

    state.send_keys(
        "New York"
    )

    # -----------------------------------------------------
    # Zip Code
    # -----------------------------------------------------

    zip_code = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "inputZip")
        )
    )

    zip_code.clear()

    zip_code.send_keys(
        "10001"
    )

    # -----------------------------------------------------
    # Submit Form
    # -----------------------------------------------------

    submit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[@id='seleniumform']/div[6]/button"
            )
        )
    )

    # -----------------------------------------------------
    # Scroll to submit button
    # -----------------------------------------------------

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        submit
    )

    submit.click()

    # -----------------------------------------------------
    # Validate Success Message
    # -----------------------------------------------------

    success = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains("
                "text(),"
                "'Thanks for contacting us, we will get back to you shortly.'"
                ")]"
            )
        )
    )

    assert (
        "Thanks for contacting us, we will get back to you shortly."
        in success.text
    )