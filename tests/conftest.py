import os

import pytest
from dotenv import load_dotenv
from selene.support.shared import browser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from python_reqres_in.framework.demo_qa import DemoQaWithEnv
from python_reqres_in.utils import attach

load_dotenv()

LOGIN = os.getenv("DEMOSHOP_LOGIN")
PASSWORD = os.getenv("DEMOSHOP_PASSWORD")


def pytest_addoption(parser):
    parser.addoption("--env")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='session')
def demoshop(env):
    return DemoQaWithEnv(env)


@pytest.fixture(scope='session')
def reqres(env):
    return DemoQaWithEnv(env).session_reqres


@pytest.fixture(scope='session')
def cookie(demoshop):
    response = demoshop.login(email=LOGIN, password=PASSWORD)
    return response.cookies.get("NOPCOMMERCE.AUTH")


@pytest.fixture(scope='function')
def app(demoshop, cookie):

    options = Options()

    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    login = os.getenv('SELENOID_LOGIN')
    password = os.getenv('SELENOID_PASSWORD')

    browser.config.driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
        options=options
    )
    browser.config.base_url = demoshop.demoqa.url
    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie(
        {"name": "NOPCOMMERCE.AUTH", "value": cookie}
    )

    yield browser

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)
    browser.quit()
